# 宿題（発展）：Claude Code の MCP 設定と演習の `app/mcp_servers.json` の比較

- 取り組んだレベル：発展
- 選んだソフトウェア：Claude Code
- 例にした MCP サーバー：Serena（コードを記号（クラス・関数）単位で検索・編集するサーバー。ファイル全体を読まずに必要な部分だけを扱えるので、トークンを節約できる）
- 調べた日付：2026-11-27
- 参照した公式ドキュメント：https://code.claude.com/docs/en/mcp

## 比べた 2 つの設定

演習で使った `app/mcp_servers.json`（STEP 4 まで終えた状態）：

```json
{
  "mcpServers": {
    "glossary": {
      "command": "uv",
      "args": ["run", "python", "-m", "app.mcp_server"]
    },
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch==2026.11.11", "--no-readability-js"]
    },
    "aws": {"url": "https://knowledge-mcp.global.api.aws"}
  }
}
```

Claude Code での Serena の設定（`mcpServers` の中の 1 項目）：

```json
"serena": {
  "type": "stdio",
  "command": "serena",
  "args": [
    "start-mcp-server",
    "--context=claude-code",
    "--project-from-cwd"
  ],
  "env": {}
}
```

## 調べた 4 つのこと

| 調べること | 演習（`app/mcp_servers.json`） | Claude Code |
|---|---|---|
| 設定を書く場所 | `app/mcp_servers.json` の 1 ファイルだけ。`app/mcp_agent.py` がこのファイルを読む | 範囲（scope）ごとに置き場所が違う。local と user は `~/.claude.json`、project はリポジトリ直下の `.mcp.json`。ファイルを直接書くほか、`claude mcp add` コマンドで登録できる |
| コマンドで起動する書き方 | `"command"` と `"args"`。`"env"` も書ける（`mcp_agent.py` がサーバーの起動に渡す） | `"type": "stdio"` に、`"command"`・`"args"`・`"env"` を書く。コマンドでは `claude mcp add --transport stdio <名前> -- <コマンド> [引数...]` |
| URL で接続する書き方 | `"url"` だけを書く | `"type": "http"` と `"url"` を書く。認証用の `"headers"` も書ける。コマンドでは `claude mcp add --transport http <名前> <URL>` |
| 有効になる範囲 | このリポジトリの `app.mcp_agent` を実行したときだけ | local（既定）：自分だけ・そのプロジェクトだけ。project：`.mcp.json` を Git で共有し、プロジェクトの全員が使う。user：自分だけ・すべてのプロジェクト |

## 違いと共通点

共通点：
- どちらも `mcpServers` の中に「サーバー名: 設定」を並べる形。Serena の項目に書かれている `command`・`args`・`env` は、演習の設定と同じ名前・同じ意味
- コマンドで起動する（stdio）か、URL に接続する（HTTP）かの 2 通りがある点も同じ。演習の `glossary`・`fetch`・Serena は、どれも自分の環境でサーバーをコマンドとして起動する stdio のサーバー

違い：
1. **接続方式の書き方**：演習の設定には `"type"` がなく、`mcp_agent.py` は `"url"` があれば HTTP、なければ `"command"` で起動すると判定する。Claude Code は `"type"`（`stdio`・`http` など）で方式を明示する。ドキュメントによると、`"url"` があっても `"type"` のない項目は stdio として扱われ、エラーになって読み込まれない。演習の `"aws": {"url": ...}` は、そのままでは Claude Code で使えない
2. **設定の置き場所と範囲**：演習は 1 ファイルで、範囲はこのリポジトリだけ。Claude Code は local・project・user の 3 つの範囲があり、同じ名前のサーバーが複数の範囲にあると、local → project → user の順に優先される。項目は範囲をまたいで混ぜられず、優先された範囲の項目がそのまま使われる
3. **登録のしかた**：演習はファイルを手で書き換える（STEP 3・4 で `,` の付け忘れに注意した）。Claude Code は `claude mcp add`・`claude mcp list`・`claude mcp remove` のようなコマンドで登録・確認・削除でき、JSON の書き間違いを避けられる
4. **使う前の確認**：Claude Code は、リポジトリの `.mcp.json` に書かれたサーバーを使う前に、使ってよいかを利用者に確認する。演習の `mcp_agent.py` には確認がなく、設定ファイルに書いたサーバーはすぐ起動・接続する
5. **環境変数の展開**：Claude Code の設定には `${VAR}` や `${VAR:-既定値}` を書け、API キーなどを設定ファイルに直接書かずに済む。演習の `mcp_agent.py` は、書いた値をそのまま使う
6. **ツール名の付け方**：演習では `glossary_search_glossary` のように「サーバー名」＋「`_`」＋「ツール名」。Claude Code では `mcp__<サーバー名>__<ツール名>` の形と読み取れる（ドキュメントの `/mcp` の説明に例として出ている）。どちらもサーバー名を付けて、同じ名前のツールを区別している

## Serena の設定から読み取れること

- `"command": "serena"` と `"args": ["start-mcp-server", ...]` で、Serena をコマンドとして起動する。演習の `fetch` を `uvx` で起動したのと同じ stdio の使い方
- `--context=claude-code` は、Claude Code から使う前提で、公開するツールや説明文を選ぶ指定と考えられる
- `--project-from-cwd` は、起動したときの作業フォルダをプロジェクトとして扱う指定と考えられる。Claude Code はプロジェクトのフォルダで起動するので、そのリポジトリのコードが対象になる。このリポジトリにある `.serena/project.yml` は、Serena がプロジェクトごとの設定を置く場所
- `"env": {}` は、追加で渡す環境変数がないことを表す。Serena は API キーなどを必要としない
- 貼り付けた項目には `"type": "stdio"` があり、Claude Code の書き方になっている。演習の `mcp_agent.py` は `"type"` を見ていないので、同じ項目を `app/mcp_servers.json` に書いても `"command"` で起動するものとして扱われる

## 確かめたこと・確かめていないこと

- 確かめたこと：この環境に `serena` コマンドが入っていること（`Serena 2.0.0`）
- 確かめたこと：この環境の `~/.claude.json`（local・user の範囲）とリポジトリの `.mcp.json`（project の範囲）には、Serena の設定は見つからなかった。貼り付けた設定が、どの範囲に書かれたものかは未確認
- 確かめていないこと：Serena を `app/mcp_servers.json` に足して `app.mcp_agent --list-tools` を実行し、ツールの一覧を表示すること（API キー不要で試せる）

## 気づき・疑問

（未記入）
