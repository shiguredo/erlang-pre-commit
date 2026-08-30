"""ダウンロード済みの efmt / elint バイナリを exec するコンソールエントリポイント。"""

from __future__ import annotations

import os
import sys

from erlang_pre_commit._binary import ensure_binary


def _exec(tool: str) -> None:
    binary = ensure_binary(tool)
    os.execv(binary, [str(binary), *sys.argv[1:]])


def efmt() -> None:
    _exec("efmt")


def elint() -> None:
    _exec("elint")
