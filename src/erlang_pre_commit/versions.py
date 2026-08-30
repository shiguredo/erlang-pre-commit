"""ピン留めした efmt / elint のバージョンとリリースアセットのチェックサム。"""

from __future__ import annotations

# ツールバージョン (先頭の "v" は付けない)
EFMT_VERSION = "0.21.0"
ELINT_VERSION = "0.1.0"

# GitHub リリースのタグ
EFMT_RELEASE_TAG = "0.21.0"
ELINT_RELEASE_TAG = "v0.1.0"

# リリースアセットの sha256: tool -> rust target -> digest
CHECKSUMS: dict[str, dict[str, str]] = {
    "efmt": {
        "aarch64-apple-darwin": (
            "e354e70c726ce24819bc781195e19567bc68a0e93d9ad8a1a84d199eded880c9"
        ),
        "x86_64-unknown-linux-musl": (
            "33073c67e8d8c73097ddbd2f555f6893d7d96109f25e4abd71e85bea1aca64ae"
        ),
    },
    "elint": {
        "aarch64-apple-darwin": (
            "eed000a4365dee76450e38c3fb031e9b9119514627a40c37bdd7c4ac7af46d1c"
        ),
        "aarch64-unknown-linux-musl": (
            "604a490baf09d1cec887c8d9fae4dc1b6da57232f4814b03760bd140c2d4e12b"
        ),
        "x86_64-unknown-linux-musl": (
            "5db517f934355a1c084d8a2e55fdd441e1bac44d109c6241ce24b4a22cf0ff05"
        ),
    },
}
