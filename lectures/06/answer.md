# 第6回 解答

## 演習

<!-- [tool call] の行は、表示された行をそのまま貼り付けてください。終わらなかった STEP は、空欄のままでかまいません。 -->

- STEP 1 のツールの名前：glossary_search_glossary
- STEP 2 の [tool call]：`[tool call]   glossary_search_glossary({'query': '3レベル'})`
- STEP 3 の [tool call]：`[tool call]   fetch_fetch({'url': 'https://modelcontextprotocol.io/'})`
- STEP 4 の [tool call]：
  - `[tool call]   aws_aws___search_documentation({'topics': ['general'], 'search_phrase': 'Amazon S3 バージョニング 概要'})`
  - `[tool call]   aws_aws___search_documentation({'search_phrase': 'Using versioning in S3 buckets Amazon S3 developer guide', 'topics': ['general']})`
- 気づき・疑問：
  - エージェントのコード（`app/mcp_agent.py`）は変えず、`app/mcp_servers.json` に数行足すだけでツールが増えた（1個 → 2個 → 7個）。`glossary`・`fetch` は自分の環境でコマンドとして起動し、`aws` は URL に接続するだけで、検索語は AWS に送られる
  - ツール名は「設定ファイルのサーバー名」＋「`_`」＋「サーバー側のツール名」。`aws_aws___search_documentation` は、サーバー名 `aws` とサーバー側の名前 `aws___search_documentation` がつながったもの
  - モデルは質問に合うツールだけを選んで呼んだ。STEP 4 では、1 回目の日本語の検索で的外れな結果が上位に来たため、英語に言い換えて検索し直した（モデル応答 3 回）
  - 外部サーバーの説明文は、作者が書いた文がそのままモデルに届く。`fetch_fetch` の説明文には「もともとインターネットにアクセスできず断るよう指示されていたが、このツールでアクセスできるようになった」という、モデルの振る舞いを変えようとする一文があった。足す前に提供元と中身を確かめる必要があると感じた
  - 入力トークンが STEP 2：709 → STEP 3：2,224 → STEP 4：11,354 と増えた。取得した本文に加えて、ツールの説明文も毎回モデルに渡るため、ツールを足すほど、使わない質問でもコストが増えるのではないか
  - 疑問：関係する回がない質問で、STEP 3 は回答の最後が「（関連する回：第N回）」のまま出て、STEP 4 は何も付かなかった。指示文の「回答の最後に、関係する回（第N回）を示す」を、外部ツールを使う質問ではどう書き分けるとよいか

## 宿題

<!-- 基礎・実装・発展のどれか1つに取り組めば完了です。 -->

- 取り組んだレベル：発展
- やったこと：
  - 自分が使っている Claude Code を選び、MCP サーバーの設定方法を公式ドキュメントで調べた（調べた日付：2026-11-27、参照：https://code.claude.com/docs/en/mcp）
  - Claude Code での設定の例として Serena（コードを記号単位で検索・編集し、トークンを節約できる MCP サーバー）の設定を取り上げ、演習で使った `app/mcp_servers.json` と比べた
  - 詳しい比較は `lectures/06/homework_answer.md` にまとめた
- 結果：

  Claude Code での Serena の設定：

  ```json
  "serena": {
    "type": "stdio",
    "command": "serena",
    "args": ["start-mcp-server", "--context=claude-code", "--project-from-cwd"],
    "env": {}
  }
  ```

  | 調べること | 演習（`app/mcp_servers.json`） | Claude Code |
  |---|---|---|
  | 設定を書く場所 | `app/mcp_servers.json` の 1 ファイルだけ（`app/mcp_agent.py` が読む） | local と user は `~/.claude.json`、project はリポジトリ直下の `.mcp.json`。`claude mcp add` コマンドでも登録できる |
  | コマンドで起動する書き方 | `"command"` と `"args"`（`"env"` も書ける） | `"type": "stdio"` に `"command"`・`"args"`・`"env"`。コマンドでは `claude mcp add --transport stdio <名前> -- <コマンド> [引数...]` |
  | URL で接続する書き方 | `"url"` だけ | `"type": "http"` と `"url"`（認証用の `"headers"` も書ける）。コマンドでは `claude mcp add --transport http <名前> <URL>` |
  | 有効になる範囲 | このリポジトリで `app.mcp_agent` を実行したときだけ | local（既定）：自分だけ・そのプロジェクトだけ／project：`.mcp.json` を Git で共有し全員が使う／user：自分だけ・すべてのプロジェクト |

  - 共通点：どちらも `mcpServers` の中に「サーバー名: 設定」を並べる形で、`command`・`args`・`env` の意味も同じ。Serena は、演習の `glossary`・`fetch` と同じく、自分の環境でコマンドとして起動する stdio のサーバー
  - 違い：Claude Code は接続方式を `"type"` で明示する。`"type"` がなく `"url"` だけの項目はエラーになって読み込まれないので、演習の `"aws": {"url": ...}` はそのままでは使えない。また、同じ名前のサーバーが複数の範囲にあると local → project → user の順に優先され、`.mcp.json` のサーバーは使う前に利用者に確認する。設定には `${VAR}` のように環境変数を書ける
- 気づき・疑問：
  - 演習の `mcp_agent.py` は `"url"` の有無だけで接続方式を決めていた。Claude Code は `"type"` で明示するので、同じ `mcpServers` 形式でも、ソフトウェアごとにそのまま使い回せるとは限らないと分かった
  - 演習の設定は 1 ファイルだけだったが、Claude Code は範囲が 3 つあり、チームで共有する設定（project）と自分だけの設定（local・user）を分けられる。API キーのような値は、`${VAR}` を使えば共有ファイルに直接書かずに済む
  - Claude Code は `.mcp.json` のサーバーを使う前に利用者に確認する。演習の補足で学んだ「信頼できるサーバーかを確かめてから足す」を、ソフトウェアの側でも支えていると感じた
  - 疑問：Serena の `--context=claude-code` や `--project-from-cwd` は、Claude Code 以外のソフトウェアや演習の `app.mcp_agent` から起動したとき、公開されるツールがどう変わるのか
