"""ピン留めした efmt / elint / ELP のバージョンとリリースアセットのチェックサム。"""

from __future__ import annotations

# ツールバージョン (先頭の "v" は付けない)
EFMT_VERSION = "0.21.1"
ELINT_VERSION = "0.1.1"
# ELP は日付ベースのタグを使う (リリースタグとバージョンが同一)
ELP_VERSION = "2026-11-20"

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
        "45d185fe2ddae79df5e50e10254520be0dd86f181c43af8f9f5ba9e3f549440d"
    ),
    "macos-x86_64-apple-darwin": (
        "eb5a267bebd33642791c684c46d3caadd669e336819a804d113bfd67a9183dcd"
    ),
    "linux-x86_64-unknown-linux-gnu": (
        "30f726acc7a1a941bffdb4c117d7a147fcf10c9b302fa8cd71bd31dae3bc28d2"
    ),
    "linux-aarch64-unknown-linux-gnu": (
        "b17aebea19a3fac8bc2c6c15f1267c8926df4c18c8791637c7a231a76322340c"
    ),
}

# ELP のリリースアセットから取り出した elp バイナリの sha256: target -> digest
# キャッシュ済みバイナリの検証に使う (アーカイブの digest とは別物)
ELP_BINARY_CHECKSUMS: dict[str, str] = {
    "macos-aarch64-apple-darwin": (
        "b11c4aba12a9ddb2821241ea378fdf7d66e07d512caa2697f0590b4648daaaa8"
    ),
    "macos-x86_64-apple-darwin": (
        "f4315729993982b55ec0a55f288aaec2c37ad0eb9064ca87d2444bac91dab34f"
    ),
    "linux-x86_64-unknown-linux-gnu": (
        "b9e4ad78dc6527aef7d6f042dd909972cbad68d4c100413d4485614a3d38f8cd"
    ),
    "linux-aarch64-unknown-linux-gnu": (
        "61ee40e163d578ea06d1d8f857b81c11971609c8807cb898c9921039bbd2beae"
    ),
}
