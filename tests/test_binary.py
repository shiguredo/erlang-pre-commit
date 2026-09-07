"""_binary モジュールの単体テスト。"""

from __future__ import annotations

import hashlib
import os
import stat
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from erlang_pre_commit._binary import _publish_binary


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
