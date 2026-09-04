"""ピン留めした efmt / elint のバージョンとリリースアセットのチェックサム。"""

from __future__ import annotations

# ツールバージョン (先頭の "v" は付けない)
EFMT_VERSION = "0.21.1"
ELINT_VERSION = "0.1.1"

# GitHub リリースのタグ
EFMT_RELEASE_TAG = "v0.21.1"
ELINT_RELEASE_TAG = "v0.1.1"

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
            "e7d10e21831e42a97a35cc15669e2e20624a374ef691184d7912dac5e99a141d"
        ),
        "aarch64-unknown-linux-musl": (
            "ee3e8c04e643b1f39d06ada524ee7cce7fd9cef4658e7df51ad28ed46070074b"
        ),
        "x86_64-unknown-linux-musl": (
            "4d838060ae3a054e41c90f8b4a670645a5c9a34f4243bded30e478e6b3d719c0"
        ),
    },
}
