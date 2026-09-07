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

## 2026.3.1

**リリース日**: 2026-09-07

- [FIX] prek が efmt / elint を並列起動した初回ダウンロードで一時ファイルが衝突しないようにする
  - `Path.with_suffix(".tmp")` により一時名が `efmt-0.21.tmp` へ潰れ、`FileNotFoundError` や `Exec format error` が起きていた
  - @voluntas

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
