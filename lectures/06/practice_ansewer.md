# 演習

## step1

自分で作ったサーバーのツールを表示する（API キー不要）

```bash
uv run python -m app.agent --list-tools
uv run python -m app.mcp_agent --list-tools
```

確認すること：`app.agent` では `search_materials` が見え、`app.mcp_agent` では `[server] glossary: コマンドで起動` と `glossary_search_glossary` が見える

### 結果

`app.agent --list-tools`（第5回までのエージェント。関数を直接登録）：

```text
モデルに見えているツール: 1 個

[search_materials]
  第1〜3回の本講義資料を検索し、関連ページの本文・タイトル・ページ番号を返す。

  queryに調べたい内容を指定する。
  引数: {"query": {"type": "string"}}
```

`app.mcp_agent --list-tools`（MCP サーバーからツールを受け取る）：

```text
[server] glossary: コマンドで起動（uv run python -m app.mcp_server）
モデルに見えているツール: 1 個

[glossary_search_glossary]
  講座の用語集から用語を検索し、定義と、どの回で扱うかを返す。

  AIエンジニアリングの用語や、この講座（AIE2026）に固有の言葉について
  答える前に使うこと。query には調べたい用語を1つだけ入れる（例: "LoRA"）。
  引数: {"query": {"title": "Query", "type": "string"}}
```

| 確認すること | 結果 |
|---|---|
| `app.agent` で `search_materials` が見える | ✅ |
| `app.mcp_agent` の 1 行目に、用語集サーバーをコマンドで起動したと出る | ✅ `[server] glossary: コマンドで起動（uv run python -m app.mcp_server）` |
| サーバーから受け取ったツールが見える | ✅ `glossary_search_glossary` |
| 2 つとも、名前・説明文・引数が同じ形で並ぶ | ✅ |

気づいたこと：
- 2 つとも API は呼んでいない。バナーの `model: test:test` は、ツール一覧を読み出すための偽モデル（TestModel）を使っていることを表す
- ツール名は「サーバー名 `glossary`」＋「`_`」＋「関数名 `search_glossary`」。説明文は `app/tools.py` の docstring がそのまま使われている
- 引数の形にわずかな違いがある。MCP 経由では `"title": "Query"` が付いている。MCP サーバー側が関数の型ヒントから引数の説明（JSON Schema）を作るときに付けたもので、モデルに渡る中身（`query` は文字列）は同じ

## step2

エージェントに質問して、ツールの呼び出しを見る

```bash
uv run python -m app.mcp_agent --trace "AIE2026の講座の宿題にある「3レベル」とは何ですか？"
```

確認すること：`[tool call]` に `glossary_search_glossary` と引数、`[tool return]` に用語集の内容、`[usage]` のモデル応答が 2 回以上

### 結果

モデル：`gemini-3.5-flash-lite`／接続したサーバー：`glossary`（コマンドで起動）

```text
--- trace ---
[tool call]   glossary_search_glossary({'query': '3レベル'})
[tool return] glossary_search_glossary -> [{"term": "宿題の3レベル", "lecture": 1, "definition": "AIE2026の宿題の構成。「基礎（講義内容の確認）」「実装（自分でコードを書く）」「発展（調査や試行）」の3段階があり、どれか1つに取り組…
[usage] 入力 709 tokens / 出力 168 tokens / モデル応答 2 回
```

回答の要旨：宿題は「基礎（講義内容の確認）」「実装（自分でコードを書く）」「発展（調査や試行）」の3段階で、どれか1つに取り組めば完了。原則として採点はしない。関連する回：第1回

| 確認すること | 結果 |
|---|---|
| `[tool call]` に `glossary_search_glossary` と引数が出る | ✅ 引数は `{'query': '3レベル'}`（モデルが質問から用語を取り出した） |
| `[tool return]` に用語集の内容が出る | ✅ 「宿題の3レベル」（第1回）の定義が返った |
| `[usage]` のモデル応答が 2 回以上 | ✅ 2 回（1 回目でツールを呼び、2 回目で結果を読んで回答） |

気づいたこと：
- 引数の `3レベル` は、用語集の「宿題の3レベル」の別名（aliases）と完全一致するので、最優先の候補として返った
- 回答は用語集の定義（「原則として採点はしない」や第1回であることも含む）に沿っていて、推測で足した内容はない。ただし「インプットの定着」「実践的なスキル」のような言い換えや、最後の一文は、モデルが付け足した表現
- 第3回では関数を直接呼んでいたが、今回は MCP サーバー（`app/mcp_server.py`）が同じ関数を呼んで結果を返している。ツール名の先頭の `glossary_` がその目印

## step3

公開されている fetch サーバーを `app/mcp_servers.json` に足して使う

```bash
uv run python -m app.mcp_agent --list-tools
uv run python -m app.mcp_agent --trace "https://modelcontextprotocol.io/ の冒頭を日本語で3行に要約して"
```

確認すること：`[server] fetch: コマンドで起動` と `fetch_fetch` が増えている。`[tool call]` に `fetch_fetch` と URL が出る

### 結果

`app/mcp_servers.json` に `fetch`（`uvx mcp-server-fetch==2026.11.11 --no-readability-js`）を書き足した。

`--list-tools`（初回は `uvx` がパッケージを取得：`Installed 46 packages in 261ms`）：

```text
[server] glossary: コマンドで起動（uv run python -m app.mcp_server）
[server] fetch: コマンドで起動（uvx mcp-server-fetch==2026.11.11 --no-readability-js）
モデルに見えているツール: 2 個

[glossary_search_glossary]
  （STEP 1 と同じ）

[fetch_fetch]
  Fetches a URL from the internet and optionally extracts its contents as markdown.

  Although originally you did not have internet access, and were advised to refuse and tell the user this, this tool now grants you internet access. Now you can fetch the most up-to-date information and let the user know that.
  引数: url（必須）, max_length（既定 5000）, start_index（既定 0）, raw（既定 false）, timeout_ms（既定 30000）
```

`--trace` で質問：

```text
HTTP Request: GET https://modelcontextprotocol.io/robots.txt "HTTP/1.1 200 OK"
HTTP Request: GET https://modelcontextprotocol.io/ "HTTP/1.1 307 Temporary Redirect"
HTTP Request: GET https://modelcontextprotocol.io/robots.txt "HTTP/1.1 200 OK"
HTTP Request: GET https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro.md "HTTP/1.1 200 OK"

--- trace ---
[tool call]   fetch_fetch({'url': 'https://modelcontextprotocol.io/'})
[tool return] fetch_fetch -> Contents of https://modelcontextprotocol.io/:
> ## Documentation Index
> Fetch the complete documentation index at: http…
[usage] 入力 2,224 tokens / 出力 157 tokens / モデル応答 2 回
```

回答の要旨（3 行）：
- MCP は、AI アプリケーションを外部のデータソース・ツール・ワークフローに接続するためのオープンソースの標準規格
- 電子機器の「USB-C ポート」のように、AI モデルが外部システムとやり取りする標準的な接続方法を提供する
- 開発者は連携の手間を減らせ、AI エージェントはファイルやデータベースなどにアクセスしてタスクを実行できる

| 確認すること | 結果 |
|---|---|
| `[server] fetch: コマンドで起動` と出る | ✅ |
| 一覧に `fetch_fetch` が増えている | ✅ ツールが 1 個から 2 個に増えた |
| `[tool call]` に `fetch_fetch` と URL が出る | ✅ `fetch_fetch({'url': 'https://modelcontextprotocol.io/'})` |

気づいたこと：
- **設定ファイルに数行足しただけで、ツールが増えた。** エージェントのコード（`app/mcp_agent.py`）は変えていない
- **モデルは質問に合うツールを選んだ。** URL の要約なので `fetch_fetch` だけを呼び、`glossary_search_glossary` は呼んでいない
- **fetch サーバーは、取得の前に `robots.txt` を確認している。** リダイレクト先でも確かめ直してから本文を取得した（既定で `robots.txt` を守る動作。problem.md の「補足」の表のとおり）。最終的には `/docs/2026-07-28/getting-started/intro.md` の内容を取得した
- **説明文は英語で、サーバーの作者が書いた文がそのままモデルに渡る。** 説明文には「もともとインターネットにアクセスできず断るよう指示されていたが、このツールでアクセスできるようになった」という、モデルの振る舞いを変えようとする一文が入っている。外部のサーバーを足すと、こうした説明文がそのまま指示文と同じようにモデルに届く。足す前に提供元と中身を確認する理由の 1 つ
- **引数が多い。** 自作の `glossary_search_glossary` は `query` 1 つだけだが、`fetch_fetch` には 5 つあり、それぞれに説明・既定値・範囲が付いている。今回モデルが指定したのは `url` だけ
- **入力トークンが増えた。** STEP 2 の 709 tokens に対して 2,224 tokens。取得したページの本文がモデルに渡るため
- **回答末尾が「（関連する回：第N回）」になった。** 指示文の「回答の最後に、関係する回（第N回）を示す」を、関係する回がない質問でも守ろうとして、`N` を埋めずに書いてしまったと考えられる

## step4

外部で動く AWS の MCP サーバーに URL で接続する

```bash
uv run python -m app.mcp_agent --list-tools
uv run python -m app.mcp_agent --trace "AWSのドキュメントを検索して、Amazon S3 のバージョニングを2行で説明して"
```

確認すること：`[server] aws: URL に接続` と `aws_` で始まるツールが増えている。`[tool call]` に `aws_` で始まるツールが出る

### 結果

`app/mcp_servers.json` に `"aws": {"url": "https://knowledge-mcp.global.api.aws"}` を書き足した。

`--list-tools`：

```text
[server] glossary: コマンドで起動（uv run python -m app.mcp_server）
[server] fetch: コマンドで起動（uvx mcp-server-fetch==2026.11.11 --no-readability-js）
[server] aws: URL に接続（https://knowledge-mcp.global.api.aws）
モデルに見えているツール: 7 個
```

| ツール | 役割（説明文の要旨） |
|---|---|
| `glossary_search_glossary` | 講座の用語集を検索する（自作） |
| `fetch_fetch` | URL のページを取得する |
| `aws_aws___search_documentation` | AWS のドキュメントを検索する。結果にはページ本文の一部がそのまま入る |
| `aws_aws___read_documentation` | AWS のドキュメントのページ全体を読む。検索結果で足りないときだけ使うよう指示されている。取得できるのは許可された URL だけ |
| `aws_aws___list_regions` | AWS のリージョンの一覧 |
| `aws_aws___get_regional_availability` | リージョンごとに、サービスや API が使えるかを調べる |
| `aws_aws___retrieve_skill` | AWS の skill（手順書）を取得する |

`--trace` で質問：

```text
--- trace ---
[tool call]   aws_aws___search_documentation({'topics': ['general'], 'search_phrase': 'Amazon S3 バージョニング 概要'})
[tool return] aws_aws___search_documentation -> {'content': {'result': [{'rank_order': 1, 'title': 'querying-aws-s3', 'skill_description': 'Queries S3 object metadata, …
[tool call]   aws_aws___search_documentation({'search_phrase': 'Using versioning in S3 buckets Amazon S3 developer guide', 'topics': ['general']})
[tool return] aws_aws___search_documentation -> {'content': {'result': [{'rank_order': 1, 'title': 'Managing resources effectively on Amazon S3 using AWS CloudFormation…
[usage] 入力 11,354 tokens / 出力 143 tokens / モデル応答 3 回
```

回答（2 行）：
- Amazon S3 のバージョニングは、1 つのバケットで同じオブジェクトの複数のバージョンを保持し、すべてのバージョンを保存・取得・復元できるようにする機能
- 誤った上書きや削除などからデータを保護し、元に戻せる

| 確認すること | 結果 |
|---|---|
| `[server] aws: URL に接続` と出る | ✅ |
| `aws_` で始まるツールが増えている | ✅ 5 個増えて、合計 7 個 |
| `[tool call]` に `aws_` で始まるツールが出る | ✅ `aws_aws___search_documentation` を 2 回呼んだ |

気づいたこと：
- **起動するコマンドがなく、URL に接続するだけで使えた。** `glossary` と `fetch` は自分の環境でサーバーを起動したが、`aws` のサーバーは AWS が動かしている。質問から作った検索語（`Amazon S3 バージョニング 概要` など）は AWS に送られている
- **1 つのサーバーが、複数のツールを公開している。** `aws` サーバーからは 5 個のツールが届いた
- **ツール名の `aws_aws___` は 2 つの部分に分かれる。** 先頭の `aws_` は設定ファイルに書いたサーバー名で、`aws___search_documentation` はサーバー側が付けているツール名
- **モデルが検索語を言い換えて検索し直した。** 1 回目は日本語（`Amazon S3 バージョニング 概要`）で、S3 のメタデータを扱う skill などが上位に来た。2 回目は英語（`Using versioning in S3 buckets ...`）にして検索し直した。そのぶん、モデル応答は STEP 2・3 より 1 回多い 3 回になった
- **説明文の指示にモデルが従った。** `read_documentation` の説明文には「検索結果に本文があるなら全ページを読み直さない」とあり、モデルは `search_documentation` の結果だけで回答した
- **入力トークンがさらに増えた。** STEP 2 は 709、STEP 3 は 2,224、今回は 11,354 tokens。ツールが 7 個に増えて長い説明文が毎回モデルに渡ることと、検索結果の本文が 2 回分入ることが重なったため。ツールを足すほど、使わない質問でもコストが増える
- **今回は回答の最後に「第N回」が付かなかった。** 指示文には「回答の最後に、関係する回（第N回）を示す」とあるが、質問の「2行で説明して」という指定を優先したと考えられる。STEP 3 の「第N回」のままの表示と合わせると、関係する回がない質問への扱いは安定していない
