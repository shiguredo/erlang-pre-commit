# 変更履歴

- CHANGE
  - 下位互換のない変更
- ADD
  - 下位互換がある追加
- UPDATE
  - 下位互換がある変更
- FIX
  - バグ修正

## develop

## 2026.3.0

**リリース日**: 2026-09-04

- [UPDATE] elint を 0.1.1 に更新する
  - @voluntas

## 2026.2.0

**リリース日**: 2026-08-30

- [ADD] efmt の Linux musl aarch64 バイナリに対応する
  - @voluntas
- [UPDATE] efmt を 0.21.1 に更新する
  - @voluntas

## 2026.1.0

**リリース日**: 2026-08-30

- [ADD] efmt / elint 向けの prek フックを追加する
  - `efmt` / `efmt-check` / `elint` を提供する
  - GitHub Releases からバイナリを取得し SHA-256 で検証する
  - 対応プラットフォームは macOS aarch64 と Linux musl (x86_64 / aarch64、efmt の Linux aarch64 は上流未提供のため除く)
  - @voluntas
