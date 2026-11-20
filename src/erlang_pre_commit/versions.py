"""ピン留めした efmt / elint / ELP のバージョンとリリースアセットのチェックサム。"""

from __future__ import annotations

# ツールバージョン (先頭の "v" は付けない)
EFMT_VERSION = "0.21.1"
ELINT_VERSION = "0.1.1"
# ELP は日付ベースのタグを使う (リリースタグとバージョンが同一)
ELP_VERSION = "2026-10-14"

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

# eqwalizer は Erlang/OTP 29 系のみを対象とする
# アセット名は ELP がビルドした OTP の版であり、メジャー番号とは一致しない
ELP_OTP_RELEASE = "29"
ELP_OTP_ASSET = "29.1"

# ELP のリリースアセット (tar.gz) の sha256: target -> digest
ELP_ARCHIVE_CHECKSUMS: dict[str, str] = {
    "macos-aarch64-apple-darwin": (
        "3311edc6b4c1d6ed7cb6a8a4e37e3d8d19ffe879d006162d33753d2c72fdcdd4"
    ),
    "macos-x86_64-apple-darwin": (
        "2eb4b2a7a17ff96f71ff456175db7c0cc265a1cee1e616ddbfb0c02771b51ed0"
    ),
    "linux-x86_64-unknown-linux-gnu": (
        "3251f2d3550adf28f33529686103fabb1fbf0b0e7deb5cd06b93dab06b8647ea"
    ),
    "linux-aarch64-unknown-linux-gnu": (
        "c15b7760222d9fed417b996790cd14aaf949fbe3ef113240bddc2fa7e73aec21"
    ),
}

# ELP のリリースアセットから取り出した elp バイナリの sha256: target -> digest
# キャッシュ済みバイナリの検証に使う (アーカイブの digest とは別物)
ELP_BINARY_CHECKSUMS: dict[str, str] = {
    "macos-aarch64-apple-darwin": (
        "d1e20d949ccc586f49633988ab06ec3465f06250e7847f0b2ff5dac948493519"
    ),
    "macos-x86_64-apple-darwin": (
        "28e75159ed88f57f08d76f30e485e0054e3ac43f3b89acb0071ac0fb66f1911f"
    ),
    "linux-x86_64-unknown-linux-gnu": (
        "2d06f74f96eac6a1004a63e101eece1a1faf2dc4c18b0b7f691a640b893ec079"
    ),
    "linux-aarch64-unknown-linux-gnu": (
        "aca9382ba90b042497c4e4503f92b0a78288d4e76dc1f7d5eb72e04f699de1e0"
    ),
}
