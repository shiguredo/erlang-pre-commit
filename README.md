# erlang-pre-commit

[![GitHub tag](https://img.shields.io/github/tag/shiguredo/erlang-pre-commit.svg)](https://github.com/shiguredo/erlang-pre-commit)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

- [efmt](https://github.com/sile/efmt) と [elint](https://github.com/sile/elint) を [prek](https://prek.j178.dev/) から利用するためのフックです
- Python パッケージとして配布しますが、実体のバイナリは PyPI ではなく GitHub Releases から取得します
- 初回実行時に対象プラットフォーム向けのバイナリをダウンロードし、SHA-256 で検証したうえで実行します

## フック

- `efmt` — `efmt -w` でフォーマットする（`*.erl` / `*.hrl` / `*.app.src` / `rebar.config`）
- `efmt-check` — `efmt -c` でフォーマットを検査する（書き込みなし）
- `elint` — `elint` でリントする（`*.erl` / `*.hrl`）

## prek.toml

```toml
[[repos]]
repo = "https://github.com/shiguredo/erlang-pre-commit"
rev = "2026.1.0"
hooks = [
  { id = "efmt" },
  { id = "elint" },
]
```

CI などで書き込みなしの検査だけしたい場合は `efmt-check` を使います。

```toml
[[repos]]
repo = "https://github.com/shiguredo/erlang-pre-commit"
rev = "2026.1.0"
hooks = [
  { id = "efmt-check" },
  { id = "elint" },
]
```

```bash
prek install --prepare-hooks
prek run --all-files
```

## オプション

prek の `args` に渡した引数は、そのまま `efmt` / `elint` に転送されます。

### efmt

| オプション | 説明 |
| --- | --- |
| `--parallel` | 並列でフォーマットする |
| `--default-off` | 各ファイル先頭に `% @efmt:off` があるかのように扱う |
| `--allow-partial-failure` | 構文エラーがあっても可能な範囲を整形する |
| `--disable-rebar3-mode` | `rebar.config` の `{efmt, ...}` を読まない |
| `--color` | `-c` 時に色付き diff を出す（`efmt-check` 向け） |
| `--check-line-length N` | `-c` 時に非コメント行の行長を検査する（整形はしない。`efmt-check` 向け） |

行長チェックと色付き diff の例です。

```toml
[[repos]]
repo = "https://github.com/shiguredo/erlang-pre-commit"
rev = "2026.1.0"
hooks = [
  { id = "efmt-check", args = ["--check-line-length=100", "--color"] },
  { id = "elint" },
]
```

`rebar.config` でも一部を指定できます（cwd から親方向へ探索します）。

```erlang
{efmt, [
    parallel,
    default_off,
    allow_partial_failure
]}.
```

`-e` / `--exclude-file` と `rebar.config` の `{exclude_file, "regex"}` は、パス未指定の既定収集時だけ効きます。prek は変更ファイルを渡すため、除外したい場合はフック側の `exclude` を使ってください。

```toml
hooks = [
  { id = "efmt", exclude = { glob = ["**/generated/**"] } },
]
```

### elint

| オプション | 説明 |
| --- | --- |
| `-l` / `--lint RULE` | 指定ルールだけ実行する（繰り返し可） |

利用可能なルール名は次のとおりです（詳細は `elint --list` / `elint --explain <name>`）。

- `case_over_if`
- `deep_case_nesting`
- `element_bif`
- `newline_after_arrow`
- `strict_generator`

特定ルールだけ実行する例です。

```toml
[[repos]]
repo = "https://github.com/shiguredo/erlang-pre-commit"
rev = "2026.1.0"
hooks = [
  { id = "efmt" },
  { id = "elint", args = ["--lint=element_bif", "--lint=case_over_if"] },
]
```

意図的な指摘はソース内の `-elint_expect` で抑制できます。プロジェクト設定ファイルはありません。

## 対応プラットフォーム

- macOS `aarch64` (Apple Silicon)
- Linux (musl) `x86_64`
- Linux (musl) `aarch64`（elint のみ。efmt は上流にプリビルドが無いため未対応）

Windows は非対応です。

## 要件

- [prek](https://prek.j178.dev/)
- Python 3.12 以上
- 初回実行時に GitHub Releases へのネットワークアクセス

## efmt ライセンス

[efmt](https://github.com/sile/efmt) は MIT OR Apache-2.0 です。Apache License 2.0 を含む全文は [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md) を参照してください。

```text
The MIT License

Copyright (c) 2021 Takeru Ohta <phjgt308@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

## elint ライセンス

[elint](https://github.com/sile/elint) は MIT です。

```text
The MIT License

Copyright (c) 2026 Takeru Ohta <phjgt308@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

## ライセンス

Apache License 2.0

```text
Copyright 2026 Shiguredo Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
