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

# ELP のアセットの OTP 表記: Erlang/OTP のメジャーリリース -> アセットの OTP 表記
# ELP は OTP のメジャーリリースごとに別のバイナリを配布する
# アセット名は ELP がビルドした OTP の版であり、メジャー番号とは一致しない
# 2026-10-14 では OTP 29 向けが otp-29.1 である
ELP_OTP_ASSETS: dict[str, str] = {
    "27": "27.3",
    "28": "28.5",
    "29": "29.1",
}

# ELP のリリースアセット (tar.gz) の sha256: target -> OTP 表記 -> digest
ELP_ARCHIVE_CHECKSUMS: dict[str, dict[str, str]] = {
    "macos-aarch64-apple-darwin": {
        "27.3": "b16fcae37bbae2def2163a4779ef09febd9904ec3382698a0032e118c770a7dc",
        "28.5": "e7c4c0a9876f9e17c806453627d89f13b25d22b43e0481117a6934d2a28377d7",
        "29.1": "3311edc6b4c1d6ed7cb6a8a4e37e3d8d19ffe879d006162d33753d2c72fdcdd4",
    },
    "macos-x86_64-apple-darwin": {
        "27.3": "00cafdddb5c898ed1b045101f73134b52ff153af15eee42cba89aca6dcb97c42",
        "28.5": "27f5f3ea6ab7213f0e3d9a93245dc59a501d92cc85edb11a8e421f0bdcf05e24",
        "29.1": "2eb4b2a7a17ff96f71ff456175db7c0cc265a1cee1e616ddbfb0c02771b51ed0",
    },
    "linux-x86_64-unknown-linux-gnu": {
        "27.3": "797315627b37cda882c8f9c1cd6c1207700accae504e2651e3bddfa4af4d7a73",
        "28.5": "e93c4b10a446c330c1db85a53f101bfebe88d19373b1213564c914953ddf5ec0",
        "29.1": "3251f2d3550adf28f33529686103fabb1fbf0b0e7deb5cd06b93dab06b8647ea",
    },
    "linux-aarch64-unknown-linux-gnu": {
        "27.3": "282f5f26105c6bc64e17745a38ba5718300c51072d34afbb2a03163dbc4abc71",
        "28.5": "2c30a04a746ae29400f26045ebed25277cf091512488e6dfa5727eac70d6beb9",
        "29.1": "c15b7760222d9fed417b996790cd14aaf949fbe3ef113240bddc2fa7e73aec21",
    },
}

# ELP のリリースアセットから取り出した elp バイナリの sha256: target -> OTP 表記 -> digest
# キャッシュ済みバイナリの検証に使う (アーカイブの digest とは別物)
ELP_BINARY_CHECKSUMS: dict[str, dict[str, str]] = {
    "macos-aarch64-apple-darwin": {
        "27.3": "009bb77ed63f0c58cece850dfe8c894a52dbcd3eed4e5c36557c5e8bc1b19877",
        "28.5": "01c0386d5fd500a3596f8f1d322fe5490d6f213f50eb44047564b2fe59cbf04d",
        "29.1": "d1e20d949ccc586f49633988ab06ec3465f06250e7847f0b2ff5dac948493519",
    },
    "macos-x86_64-apple-darwin": {
        "27.3": "6ae3ebf0379c1074d09d66986a97f8dadd11403821b7d5449b12924af7289502",
        "28.5": "b5aa400f1374f2e1b564d9793ec340cb575dffad16814c87185add9105da0f83",
        "29.1": "28e75159ed88f57f08d76f30e485e0054e3ac43f3b89acb0071ac0fb66f1911f",
    },
    "linux-x86_64-unknown-linux-gnu": {
        "27.3": "93b576c780280cdeb864d904918b5a9e11bbecc1878db20a01b9984bdc239b17",
        "28.5": "5198720c0ac3410c8367003cd973be5a88abb3281a301c05a06e9ef11b33cb75",
        "29.1": "2d06f74f96eac6a1004a63e101eece1a1faf2dc4c18b0b7f691a640b893ec079",
    },
    "linux-aarch64-unknown-linux-gnu": {
        "27.3": "2a5e2d9749623288fc2122fae9b3a3c7e205792987481804f496308be2c7b7b2",
        "28.5": "87fb23ce3b501666c1e705ab7613caca8e9df6c26014232bacfbd8f9cf9222df",
        "29.1": "aca9382ba90b042497c4e4503f92b0a78288d4e76dc1f7d5eb72e04f699de1e0",
    },
}
