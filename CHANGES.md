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

- [ADD] efmt / elint 向けの prek フックを追加する
  - `efmt` / `efmt-check` / `elint` を提供する
  - GitHub Releases からバイナリを取得し SHA-256 で検証する
  - 対応プラットフォームは macOS aarch64 と Linux musl (x86_64 / aarch64、efmt の Linux aarch64 は上流未提供のため除く)
  - @voluntas
