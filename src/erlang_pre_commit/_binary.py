"""GitHub Releases から efmt / elint バイナリをダウンロードする。"""

from __future__ import annotations

import fcntl
import hashlib
import os
import platform
import stat
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
)

_USER_AGENT = "shiguredo-erlang-pre-commit"


def rust_target() -> str:
    system = platform.system()
    machine = platform.machine().lower()

    if machine in ("amd64", "x86_64"):
        arch = "x86_64"
    elif machine in ("arm64", "aarch64"):
        arch = "aarch64"
    else:
        raise RuntimeError(
            f"Unsupported CPU architecture for erlang-pre-commit: {platform.machine()}"
        )

    if system == "Darwin":
        return f"{arch}-apple-darwin"
    if system == "Linux":
        return f"{arch}-unknown-linux-musl"
    raise RuntimeError(
        f"Unsupported OS for erlang-pre-commit: {system} (supported: macOS and Linux)"
    )


def release_asset_url(tool: str, version: str, release_tag: str, target: str) -> str:
    asset = f"{tool}-{version}.{target}"
    return f"https://github.com/sile/{tool}/releases/download/{release_tag}/{asset}"


def _expected_checksum(tool: str, target: str) -> str:
    try:
        return CHECKSUMS[tool][target]
    except KeyError as exc:
        raise RuntimeError(
            f"No prebuilt {tool} binary for target {target}. "
            f"Available: {', '.join(sorted(CHECKSUMS.get(tool, {})))}"
        ) from exc


def _bin_dir() -> Path:
    override = os.environ.get("ERLANG_PRE_COMMIT_BIN_DIR")
    if override:
        return Path(override)
    return Path(__file__).resolve().parent / "_bins"


def _is_ready(destination: Path, expected: str) -> bool:
    return destination.is_file() and _sha256_file(destination) == expected


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


def ensure_binary(tool: str) -> Path:
    if tool == "efmt":
        version = EFMT_VERSION
        release_tag = EFMT_RELEASE_TAG
    elif tool == "elint":
        version = ELINT_VERSION
        release_tag = ELINT_RELEASE_TAG
    else:
        raise ValueError(f"Unknown tool: {tool}")

    target = rust_target()
    expected = _expected_checksum(tool, target)
    destination = _bin_dir() / f"{tool}-{version}-{target}"

    if _is_ready(destination, expected):
        return destination

    lock_path = destination.with_name(f".{destination.name}.lock")
    with _exclusive_file_lock(lock_path):
        # 待機中に他プロセスが配置済みならダウンロードしない
        if _is_ready(destination, expected):
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


def _sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()
