"""GitHub Releases から efmt / elint / ELP バイナリをダウンロードする。"""

from __future__ import annotations

import fcntl
import hashlib
import io
import os
import platform
import shutil
import stat
import subprocess
import tarfile
import tempfile
import urllib.error
import urllib.request
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from erlang_pre_commit.versions import (
    CHECKSUMS,
    EFMT_RELEASE_TAG,
    EFMT_VERSION,
    ELINT_RELEASE_TAG,
    ELINT_VERSION,
    ELP_ARCHIVE_CHECKSUMS,
    ELP_BINARY_CHECKSUMS,
    ELP_OTP_ASSETS,
    ELP_VERSION,
)

_USER_AGENT = "shiguredo-erlang-pre-commit"

# erl から Erlang/OTP のメジャーリリースだけを取り出すための評価式
_OTP_RELEASE_EVAL = 'io:format("~s", [erlang:system_info(otp_release)]), halt(0).'

# ELP の tar.gz に含まれる実行ファイルの名前
_ELP_MEMBER = "elp"


def _normalize_arch(machine: str) -> str:
    """uname -m の値をアセットのアーキテクチャ表記へ正規化する。"""
    normalized = machine.lower()
    if normalized in ("amd64", "x86_64"):
        return "x86_64"
    if normalized in ("arm64", "aarch64"):
        return "aarch64"
    raise RuntimeError(f"Unsupported CPU architecture for erlang-pre-commit: {machine}")


def _rust_target(system: str, machine: str) -> str:
    """efmt / elint が配布する Rust target を返す。"""
    arch = _normalize_arch(machine)
    if system == "Darwin":
        return f"{arch}-apple-darwin"
    if system == "Linux":
        return f"{arch}-unknown-linux-musl"
    raise RuntimeError(
        f"Unsupported OS for erlang-pre-commit: {system} (supported: macOS and Linux)"
    )


def rust_target() -> str:
    """実行環境に対応する efmt / elint の Rust target を返す。"""
    return _rust_target(platform.system(), platform.machine())


def _elp_target(system: str, machine: str) -> str:
    """ELP が配布するアセットの target を返す。"""
    arch = _normalize_arch(machine)
    if system == "Darwin":
        return f"macos-{arch}-apple-darwin"
    if system == "Linux":
        # ELP は glibc 向けのバイナリのみ配布しており musl 向けは無い
        return f"linux-{arch}-unknown-linux-gnu"
    raise RuntimeError(f"Unsupported OS for eqwalizer: {system} (supported: macOS and Linux)")


def elp_target() -> str:
    """実行環境に対応する ELP の target を返す。"""
    return _elp_target(platform.system(), platform.machine())


def _elp_otp_asset(release: str) -> str:
    """Erlang/OTP のメジャーリリースに対応する ELP アセットの OTP 表記を返す。"""
    otp_asset = ELP_OTP_ASSETS.get(release)
    if otp_asset is None:
        supported = ", ".join(sorted(ELP_OTP_ASSETS))
        raise RuntimeError(
            f"Unsupported Erlang/OTP release for eqwalizer: {release} (supported: {supported})"
        )
    return otp_asset


def _detect_otp_release() -> str:
    """erl を起動して Erlang/OTP のメジャーリリースを取り出す。"""
    try:
        completed = subprocess.run(
            ["erl", "-noshell", "-eval", _OTP_RELEASE_EVAL],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        raise RuntimeError(
            "erl is required to run eqwalizer (supported: Erlang/OTP 27, 28 and 29)"
        ) from exc
    if completed.returncode != 0:
        raise RuntimeError(
            f"Failed to detect the Erlang/OTP release: erl exited with status "
            f"{completed.returncode}: {completed.stderr.strip()}"
        )
    release = completed.stdout.strip()
    if not release:
        raise RuntimeError("Failed to detect the Erlang/OTP release: erl produced no output")
    return release


def elp_otp_asset() -> str:
    """実行環境の Erlang/OTP に対応する ELP アセットの OTP 表記を返す。"""
    return _elp_otp_asset(_detect_otp_release())


def release_asset_url(tool: str, version: str, release_tag: str, target: str) -> str:
    asset = f"{tool}-{version}.{target}"
    return f"https://github.com/sile/{tool}/releases/download/{release_tag}/{asset}"


def elp_asset_url(target: str, otp_asset: str) -> str:
    asset = f"elp-{target}-otp-{otp_asset}.tar.gz"
    return (
        "https://github.com/WhatsApp/erlang-language-platform/releases/download/"
        f"{ELP_VERSION}/{asset}"
    )


def _expected_checksum(tool: str, target: str) -> str:
    try:
        return CHECKSUMS[tool][target]
    except KeyError as exc:
        raise RuntimeError(
            f"No prebuilt {tool} binary for target {target}. "
            f"Available: {', '.join(sorted(CHECKSUMS.get(tool, {})))}"
        ) from exc


def _elp_checksum(table: dict[str, dict[str, str]], target: str, otp_asset: str) -> str:
    checksums = table.get(target)
    if checksums is None or otp_asset not in checksums:
        raise RuntimeError(
            f"No pinned ELP checksum for target {target} with OTP {otp_asset}. "
            f"Available OTP assets: {', '.join(sorted(checksums or {}))}"
        )
    return checksums[otp_asset]


def _bin_dir() -> Path:
    override = os.environ.get("ERLANG_PRE_COMMIT_BIN_DIR")
    if override:
        return Path(override)
    return Path(__file__).resolve().parent / "_bins"


def _ensure_ready(destination: Path, expected: str) -> bool:
    """
    キャッシュ済みバイナリが利用可能かを返し、必要なら実行ビットを付与する。

    パーミッションを保持しない方法でキャッシュをコピーすると実行ビットが
    落ちることがある。digest が一致していれば再ダウンロードせずに復旧する。
    """
    if not destination.is_file() or _sha256_file(destination) != expected:
        return False
    mode = destination.stat().st_mode
    if not mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH):
        destination.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return True


@contextmanager
def _exclusive_file_lock(lock_path: Path) -> Iterator[None]:
    """
    ダウンロードと配置をプロセス間で直列化する。

    prek は同一フックを複数プロセスで並列起動するため、
    初回実行時に同じバイナリへ同時書き込みが起きる。
    """
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+b") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def _publish_binary(destination: Path, data: bytes) -> None:
    """
    検証済みバイト列を destination へ原子的に配置する。

    Path.with_suffix(".tmp") は使わない。
    `efmt-0.21.1-aarch64-apple-darwin` の suffix は
    `.1-aarch64-apple-darwin` と解釈され、一時名が
    `efmt-0.21.tmp` に潰れて並列プロセス間で衝突するため。
    加えて mkstemp でプロセス固有の一時ファイルにし、
    ロック漏れがあっても truncate 競合しないようにする。
    """
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{destination.name}.",
        suffix=".tmp",
        dir=destination.parent,
    )
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
        tmp_path.chmod(tmp_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        os.replace(tmp_path, destination)
    except BaseException:
        tmp_path.unlink(missing_ok=True)
        raise


def _download(url: str, tool: str, version: str, target: str) -> bytes:
    try:
        request = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
        with urllib.request.urlopen(request) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        raise RuntimeError(
            f"Failed to download {tool} {version} for {target} from {url}: HTTP {exc.code}"
        ) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(
            f"Failed to download {tool} {version} for {target} from {url}: {exc}"
        ) from exc


def _extract_elp(archive: bytes) -> bytes:
    """
    ELP の tar.gz から elp バイナリだけを取り出す。

    展開先をファイルシステムにせずメンバーのバイト列だけを取り出すため、
    パス走査 (path traversal) の影響を受けない。
    """
    try:
        with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as tar:
            try:
                member = tar.getmember(_ELP_MEMBER)
            except KeyError as exc:
                message = f"The ELP archive does not contain the {_ELP_MEMBER} binary"
                raise RuntimeError(message) from exc
            handle = tar.extractfile(member)
            if handle is None:
                message = f"The ELP archive entry {_ELP_MEMBER} is not a regular file"
                raise RuntimeError(message)
            return handle.read()
    except (tarfile.TarError, OSError) as exc:
        raise RuntimeError(f"Failed to read the ELP archive: {exc}") from exc


def _require_rebar3() -> None:
    """eqwalizer は rebar3 でプロジェクトを読み込むため、rebar3 の存在を確認する。"""
    if shutil.which("rebar3") is None:
        raise RuntimeError("rebar3 3.24.0 or later is required to run eqwalizer")


def _ensure_elp_binary() -> Path:
    """Erlang/OTP のバージョンに合う ELP バイナリを用意して返す。"""
    _require_rebar3()
    target = elp_target()
    otp_asset = elp_otp_asset()
    archive_checksum = _elp_checksum(ELP_ARCHIVE_CHECKSUMS, target, otp_asset)
    binary_checksum = _elp_checksum(ELP_BINARY_CHECKSUMS, target, otp_asset)
    destination = _bin_dir() / f"elp-{ELP_VERSION}-{target}-otp-{otp_asset}"

    if _ensure_ready(destination, binary_checksum):
        return destination

    lock_path = destination.with_name(f".{destination.name}.lock")
    with _exclusive_file_lock(lock_path):
        # 待機中に他プロセスが配置済みならダウンロードしない
        if _ensure_ready(destination, binary_checksum):
            return destination

        asset_target = f"{target}-otp-{otp_asset}"
        url = elp_asset_url(target, otp_asset)
        archive = _download(url, "elp", ELP_VERSION, asset_target)

        archive_digest = hashlib.sha256(archive).hexdigest()
        if archive_digest != archive_checksum:
            raise RuntimeError(
                f"Checksum mismatch for the ELP archive {ELP_VERSION} "
                f"({asset_target}): expected {archive_checksum}, got {archive_digest}"
            )

        binary = _extract_elp(archive)
        binary_digest = hashlib.sha256(binary).hexdigest()
        if binary_digest != binary_checksum:
            raise RuntimeError(
                f"Checksum mismatch for the extracted elp binary ({asset_target}): "
                f"expected {binary_checksum}, got {binary_digest}"
            )

        _publish_binary(destination, binary)
        return destination


def _ensure_release_binary(tool: str, version: str, release_tag: str) -> Path:
    """GitHub Releases のバイナリをそのまま配置して返す。"""
    target = rust_target()
    expected = _expected_checksum(tool, target)
    destination = _bin_dir() / f"{tool}-{version}-{target}"

    if _ensure_ready(destination, expected):
        return destination

    lock_path = destination.with_name(f".{destination.name}.lock")
    with _exclusive_file_lock(lock_path):
        # 待機中に他プロセスが配置済みならダウンロードしない
        if _ensure_ready(destination, expected):
            return destination

        url = release_asset_url(tool, version, release_tag, target)
        data = _download(url, tool, version, target)

        digest = hashlib.sha256(data).hexdigest()
        if digest != expected:
            raise RuntimeError(
                f"Checksum mismatch for {tool} {version} ({target}): "
                f"expected {expected}, got {digest}"
            )

        _publish_binary(destination, data)
        return destination


def ensure_binary(tool: str) -> Path:
    if tool == "efmt":
        return _ensure_release_binary("efmt", EFMT_VERSION, EFMT_RELEASE_TAG)
    if tool == "elint":
        return _ensure_release_binary("elint", ELINT_VERSION, ELINT_RELEASE_TAG)
    if tool == "elp":
        return _ensure_elp_binary()
    raise ValueError(f"Unknown tool: {tool}")


def _sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()
