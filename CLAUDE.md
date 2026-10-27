# CLAUDE.md

このファイルは、このリポジトリで作業する Claude Code (claude.ai/code) にガイダンスを提供するものです。

## このリポジトリについて

AIエンジニアリング講座（AIE2026、日本語で実施）の演習・宿題用リポジトリです。講座全体を通して
「学習支援エージェント」という1つのエージェントを少しずつ育てていく構成になっています。第1回は素の
LLM呼び出し、第3回でツール呼び出しを追加、第5回でそのツールを MCP サーバーの裏側に移します。コードの
コメントやdocstringは受講生向けに日本語で書かれています。`# TODO(第N回 演習): ...` というコメントは
意図的に未完成にしてある演習用のスタブなので、指示がない限り黙って実装を埋めたりしないでください。

## コマンド

```bash
uv sync --frozen          # 依存関係をインストール（Python 3.12、uv.lock でバージョン固定。アップグレードしない）
uv run pytest -q          # 全テストを実行（APIキー不要。pydantic_ai の TestModel を使用）
uv run pytest -q tests/test_tools.py::test_lecture_summary   # 単体テストを実行

uv run python -m app.ask "質問"                      # 第1回：ツールなしの素のLLM呼び出し
uv run python -m app.agent "質問"                     # 第3回：tools.py のツールを直接登録したエージェント
uv run python -m app.agent --trace "質問"              # ツール呼び出し・戻り値を表示
uv run python -m app.agent --mcp --trace "質問"        # 第5回：同じエージェントをMCP経由のツールで動かす
uv run python -m app.agent --mcp --list-tools         # モデルに見えるツール一覧を表示（APIキー不要）

uv run python -m app.mcp_server --http    # 用語集MCPサーバーをStreamable HTTPで起動（既定はstdio）
```

`uv run python -m app.ask`／`app.agent` の実行には環境変数 `GEMINI_API_KEY` が必要です。テストと
`--list-tools` は実際のAPIを呼ばず `pydantic_ai.models.test.TestModel` を使うため不要です。既定モデルは
`gemini-3.5-flash-lite` で、環境変数 `AIE_MODEL` で切り替えられます。

## アーキテクチャ

- `app/config.py` — `MODEL`（環境変数 `AIE_MODEL`）と `GEMINI_API_KEY` の取得を一元管理する場所。加えて
  `api_error_message()` は Gemini のHTTPステータスコード（429/503/4xxなど）を受講生向けの日本語メッセージに
  変換し、`ask.py` と `agent.py` の両方で共用されています。
- `app/tools.py` — docstringと型ヒントがそのままモデルへのツール説明文になる、素のPython関数群。
  `search_glossary` は `data/glossary.json` を読む（`@cache` でキャッシュ）、`get_lecture_summary` は
  `data/lectures/NN.md` を読みます。これらの同じ関数が、回によって2通りの方法で登録されます。
  - **第3回のパス**：`app/agent.py` が `agent.tool_plain(...)` で `pydantic_ai.Agent` に直接登録する。
  - **第5回のパス**：`app/mcp_server.py` が同じ関数を `server.tool()(...)` でMCPサーバーとして公開し、
    `app/agent.py --mcp` はその代わりに `load_mcp_servers()` でツールセットを組み立てたエージェントを作る。
    `load_mcp_servers()` は `app/mcp_servers.json`（Claude DesktopやCursorと同じ `mcpServers` 形式の設定
    ファイル）を読み、`fastmcp` の `MCPToolset`／`StdioTransport` で接続します。このパスではツール名に
    `サーバー名_` というプレフィックスが付きます。
- `app/agent.py` は実行時（`build_model()`）になってからモデル（`GoogleModel` + `GoogleProvider`）を
  組み立てます。これにより、テストはAPIキーなしで `agent.override(model=...)` から `TestModel` に
  差し替えられます。
- データ（`data/glossary.json`、`data/lectures/NN.md`）は、エージェントが推測ではなくそこに基づいて
  回答すべき「正解データ」です。`app/ask.py` の `DEFAULT_QUESTION` は意図的に講座固有の質問になっていて、
  第1回の素のLLM呼び出しではうまく答えられず、第3回以降のエージェントは用語集から正しく答えられる、
  という対比を示す設計です。

## このリポジトリ特有の決まり

- APIキーは必ず環境変数 `GEMINI_API_KEY` からのみ取得します。コードやコミットに直接書かないこと。
- `pyproject.toml`／`uv.lock` の依存バージョンは講座期間中、意図的に固定されています。指示なく
  アップグレードしないこと。
- 各 `lectures/NN/` ディレクトリには `problem.md`（課題内容）と `answer.md`（受講生が記入して提出する
  ファイル）があります。`answer.md` は受講生自身が書く内容なので、丸ごと代わりに生成するものではありません。
