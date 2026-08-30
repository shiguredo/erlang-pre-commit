"""ピン留めした efmt / elint のバージョンとリリースアセットのチェックサム。"""

from __future__ import annotations

# ツールバージョン (先頭の "v" は付けない)
EFMT_VERSION = "0.21.1"
ELINT_VERSION = "0.1.0"

# GitHub リリースのタグ
EFMT_RELEASE_TAG = "v0.21.1"
ELINT_RELEASE_TAG = "v0.1.0"

# リリースアセットの sha256: tool -> rust target -> digest
CHECKSUMS: dict[str, dict[str, str]] = {
    "efmt": {
        "aarch64-apple-darwin": (
            "621ec1bd7e316c6bb65d843c3a8dacd625cd249d29789536097755f05d9c9366"
        ),
        "aarch64-unknown-linux-musl": (
            "423ca4eaeb767490afbce4f06c381e2adf5d17ddb55fd9c7d2d9e1b8f4c00aa9"
        ),
        "x86_64-unknown-linux-musl": (
            "7aed92c87dae1ec81a95fbf1bc7035a26e5549f48a1b277a5741338cb4885f21"
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
