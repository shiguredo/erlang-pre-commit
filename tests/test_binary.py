"""_binary モジュールの単体テスト。"""

from __future__ import annotations

import hashlib
import io
import os
import stat
import tarfile
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import pytest

from erlang_pre_commit._binary import (
    _elp_otp_asset,
    _elp_target,
    _extract_elp,
    _publish_binary,
    elp_asset_url,
)
from erlang_pre_commit.versions import ELP_ARCHIVE_CHECKSUMS, ELP_BINARY_CHECKSUMS


def _worker_publish(bin_dir: str, payload: bytes, index: int) -> tuple[str, int]:
    """
    子プロセスから _publish_binary を呼び、配置結果を返す。

    ProcessPoolExecutor 経由で使うため、モジュールトップレベルに置く。
    """
    destination = Path(bin_dir) / "efmt-0.21.1-aarch64-apple-darwin"
    try:
        _publish_binary(destination, payload)
    except OSError as exc:
        return (f"error:{type(exc).__name__}:{exc}", index)
    if not destination.is_file():
        return ("error:missing", index)
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    expected = hashlib.sha256(payload).hexdigest()
    if digest != expected:
        return ("error:checksum", index)
    if not (destination.stat().st_mode & stat.S_IXUSR):
        return ("error:not-executable", index)
    return ("ok", index)


def _write_tar_gz(path: Path, members: dict[str, bytes]) -> None:
    """テスト用に ELP と同じ構造の tar.gz を組み立てる。"""
    with tarfile.open(path, "w:gz") as tar:
        for name, payload in members.items():
            info = tarfile.TarInfo(name)
            info.size = len(payload)
            info.mode = 0o755
            tar.addfile(info, io.BytesIO(payload))


def test_publish_binary_survives_parallel_writers(tmp_path: Path) -> None:
    """
    複数プロセスが同じ destination へ同時書き込みしても壊れないことを確認する。

    旧実装は with_suffix(".tmp") で一時名が `efmt-0.21.tmp` に衝突し、
    FileNotFoundError や Exec format error の原因になっていた。
    """
    payload = os.urandom(64 * 1024)
    bin_dir = tmp_path / "bins"
    bin_dir.mkdir()

    workers = 16
    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(_worker_publish, str(bin_dir), payload, index)
            for index in range(workers)
        ]
        results = [future.result() for future in as_completed(futures)]

    errors = [result for result in results if result[0] != "ok"]
    assert errors == [], f"並列配置で失敗した: {errors}"

    destination = bin_dir / "efmt-0.21.1-aarch64-apple-darwin"
    assert destination.read_bytes() == payload
    assert destination.stat().st_mode & stat.S_IXUSR


def test_with_suffix_collides_for_binary_destination_names() -> None:
    """
    バイナリ配置先名に with_suffix(".tmp") を使うと一時名が潰れることを固定する。

    3.12 / 3.13 / 3.14 いずれも同じ衝突になる。
    """
    destination = Path("efmt-0.21.1-aarch64-apple-darwin")
    assert destination.with_suffix(".tmp").name == "efmt-0.21.tmp"


def test_elp_target_returns_elp_asset_names() -> None:
    """
    ELP は efmt / elint と異なる target 表記のバイナリを配布する。

    macOS は macos-<arch>-apple-darwin、Linux は glibc 向けの
    linux-<arch>-unknown-linux-gnu になることを固定する。
    """
    assert _elp_target("Darwin", "arm64") == "macos-aarch64-apple-darwin"
    assert _elp_target("Darwin", "x86_64") == "macos-x86_64-apple-darwin"
    assert _elp_target("Linux", "x86_64") == "linux-x86_64-unknown-linux-gnu"
    assert _elp_target("Linux", "aarch64") == "linux-aarch64-unknown-linux-gnu"


def test_elp_target_rejects_unsupported_platform() -> None:
    """
    未対応の OS と CPU アーキテクチャでは、理由の分かる例外で止まることを確認する。
    """
    with pytest.raises(RuntimeError, match="Unsupported OS for eqwalizer"):
        _elp_target("Windows", "AMD64")
    with pytest.raises(RuntimeError, match="Unsupported CPU architecture"):
        _elp_target("Darwin", "riscv64")


def test_elp_otp_asset_maps_supported_releases() -> None:
    """
    ELP のアセットは OTP のメジャーリリースごとに別名なので、対応を固定する。
    """
    assert _elp_otp_asset("27") == "27.3"
    assert _elp_otp_asset("28") == "28.5"
    assert _elp_otp_asset("29") == "29"


def test_elp_otp_asset_rejects_unsupported_release() -> None:
    """
    ELP が対応していない OTP では、対応バージョンを示して失敗することを確認する。
    """
    with pytest.raises(RuntimeError, match="Unsupported Erlang/OTP release"):
        _elp_otp_asset("26")
    with pytest.raises(RuntimeError, match="Unsupported Erlang/OTP release"):
        _elp_otp_asset("30")


def test_elp_asset_url_pins_the_release_tag() -> None:
    """
    アセットの URL がピン留めした ELP のリリースタグを指すことを確認する。
    """
    assert elp_asset_url("macos-aarch64-apple-darwin", "28.5") == (
        "https://github.com/WhatsApp/erlang-language-platform/releases/download/"
        "2026-08-10/elp-macos-aarch64-apple-darwin-otp-28.5.tar.gz"
    )


def test_elp_checksums_cover_all_supported_variants() -> None:
    """
    配布している 4 target x 3 OTP のすべてで、アーカイブとバイナリの
    sha256 が揃っていることを確認する。
    """
    targets = [
        "macos-aarch64-apple-darwin",
        "macos-x86_64-apple-darwin",
        "linux-x86_64-unknown-linux-gnu",
        "linux-aarch64-unknown-linux-gnu",
    ]
    otp_assets = ["27.3", "28.5", "29"]
    for target in targets:
        for otp_asset in otp_assets:
            archive = ELP_ARCHIVE_CHECKSUMS.get(target, {}).get(otp_asset)
            binary = ELP_BINARY_CHECKSUMS.get(target, {}).get(otp_asset)
            assert archive is not None, f"{target} / OTP {otp_asset} のアーカイブの sha256 が無い"
            assert binary is not None, f"{target} / OTP {otp_asset} のバイナリの sha256 が無い"
            assert len(archive) == 64, f"{target} / OTP {otp_asset} のアーカイブの sha256 が不正"
            assert len(binary) == 64, f"{target} / OTP {otp_asset} のバイナリの sha256 が不正"


def test_extract_elp_reads_binary_from_archive(tmp_path: Path) -> None:
    """
    ELP の tar.gz から elp のバイト列だけを取り出せることを確認する。

    アーカイブ内の無関係なファイルは無視される。
    """
    payload = b"\x7fELF" + os.urandom(256)
    archive_path = tmp_path / "elp.tar.gz"
    _write_tar_gz(archive_path, {"elp": payload, "README.md": b"not a binary"})

    assert _extract_elp(archive_path.read_bytes()) == payload


def test_extract_elp_rejects_archive_without_binary(tmp_path: Path) -> None:
    """
    elp を含まない tar.gz は黙って空を返さず、理由付きで失敗することを確認する。
    """
    archive_path = tmp_path / "no-binary.tar.gz"
    _write_tar_gz(archive_path, {"README.md": b"no binary"})

    with pytest.raises(RuntimeError, match="does not contain the elp binary"):
        _extract_elp(archive_path.read_bytes())


def test_extract_elp_rejects_directory_member(tmp_path: Path) -> None:
    """
    elp という名前がディレクトリの場合は、理由付きで失敗することを確認する。
    """
    archive_path = tmp_path / "directory.tar.gz"
    with tarfile.open(archive_path, "w:gz") as tar:
        info = tarfile.TarInfo("elp")
        info.type = tarfile.DIRTYPE
        tar.addfile(info)

    with pytest.raises(RuntimeError, match="is not a regular file"):
        _extract_elp(archive_path.read_bytes())


def test_extract_elp_rejects_broken_archive() -> None:
    """
    tar.gz として壊れたデータは、展開せずに理由付きで失敗することを確認する。
    """
    with pytest.raises(RuntimeError, match="Failed to read the ELP archive"):
        _extract_elp(b"not a tar.gz")
