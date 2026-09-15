"""ピン留めした efmt / elint / ELP のバージョンとリリースアセットのチェックサム。"""

from __future__ import annotations

# ツールバージョン (先頭の "v" は付けない)
EFMT_VERSION = "0.21.1"
ELINT_VERSION = "0.1.1"
# ELP は日付ベースのタグを使う (リリースタグとバージョンが同一)
ELP_VERSION = "2026-08-10"

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

# ELP のアセットの OTP 表記: Erlang/OTP のメジャーリリース -> アセットの OTP 表記
# ELP は OTP のメジャーリリースごとに別のバイナリを配布する
ELP_OTP_ASSETS: dict[str, str] = {
    "27": "27.3",
    "28": "28.5",
    "29": "29",
}

# ELP のリリースアセット (tar.gz) の sha256: target -> OTP 表記 -> digest
ELP_ARCHIVE_CHECKSUMS: dict[str, dict[str, str]] = {
    "macos-aarch64-apple-darwin": {
        "27.3": "7317a9934edc411e94392d5cc720f2e0c18112e7959060678aaef4d6dacdd9f2",
        "28.5": "2960208a24b2b97e736e1571b350db93af0010f916d136f923904a157cc07c55",
        "29": "bd4490661df4b85f65541c9ce042142396730040486bdf35cb5df1b2bac22761",
    },
    "macos-x86_64-apple-darwin": {
        "27.3": "d7c739a6b23ba7bfc0fc8481619ec55e41257d08cb7aa8b16499fb4c4f5e38e2",
        "28.5": "3402849bb1c8355dff18ce51e81cddd67ee0fc90d449b9e1a4c8d3d1ab38d5ce",
        "29": "2451254c84aaeefb0dd928387fd5927e537767c251c282bef33d4f79dd4d273b",
    },
    "linux-x86_64-unknown-linux-gnu": {
        "27.3": "c0e672a8381b5ea787e94a872847567b10d9b4d0053ca1148f4b236f61af3c63",
        "28.5": "7732bf3f52b2fc08b6f45428fb8a14ee7a13d38ae4582e6fb4fec9176ce6e0f0",
        "29": "711ea859b9c998eb990f9e647e03029c3aa1dfb61b177e6de5bf95c69b62695b",
    },
    "linux-aarch64-unknown-linux-gnu": {
        "27.3": "0af71bd62e95998b7e57edd2083141b60edab51d0a2da988e6e71abb88cd3f34",
        "28.5": "eede711c74aa93d69fd3a1b65fb88f10169fcbffb8d2fc830486033d82f5ccef",
        "29": "91c98287f5738660766e572ecdc1dff9b06d041ead1b463f0422dc5bfc6499fc",
    },
}

# ELP のリリースアセットから取り出した elp バイナリの sha256: target -> OTP 表記 -> digest
# キャッシュ済みバイナリの検証に使う (アーカイブの digest とは別物)
ELP_BINARY_CHECKSUMS: dict[str, dict[str, str]] = {
    "macos-aarch64-apple-darwin": {
        "27.3": "cb161dbb19409dd6df3ff5e14f411f6f5f6c9d006ec28696e7f94bea292ccbbb",
        "28.5": "042bf4df864376f50a70bca9f79ea05b4cbc22067003f9a5ab7f393eb19371b3",
        "29": "7f7fb5d802a8de5a9ca59c6170ccb4c28a6978c327012a89e624fea8c1798dca",
    },
    "macos-x86_64-apple-darwin": {
        "27.3": "3f697020211985f9ebd7804a281b8e7d65a2fb487ca56eb04c02577a0ffe5ef1",
        "28.5": "01f56a58802992c44c34c2e7a49f861c243dd2feda0d02847bc5dc0a69cc5b62",
        "29": "0ac8e06baaa197417c6b043cddabc204f5b263985f7683a9f68d49743970a1be",
    },
    "linux-x86_64-unknown-linux-gnu": {
        "27.3": "46fcb470e887534e53217f3b4c2dc8e0b1c9a6b1064dd6b8dc087e0fd6b2c731",
        "28.5": "3eac7aca772cdc5d48defc77aee94fb7299b2589d1d275b7ca7563f9f6149e92",
        "29": "f3859d651c1c79774bb47b0e5589e9308a5c8552f494b1bf068af40522dfb41d",
    },
    "linux-aarch64-unknown-linux-gnu": {
        "27.3": "f65114826e3581fe8ad8d66757fbfc28a73e988e2676360795fd40c0bcb94b8f",
        "28.5": "c4690828e21e3bcc0e60e2e02535204b282dce32e220e18daf403422cdea5c1b",
        "29": "39b20e2d6c75636a304a70ce0831b2bae22600086824b4c92c5e114f28a7144e",
    },
}
