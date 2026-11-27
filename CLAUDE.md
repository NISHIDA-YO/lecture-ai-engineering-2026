# CLAUDE.md

このファイルは、このリポジトリで作業する Claude Code (claude.ai/code) にガイダンスを提供するものです。

## このリポジトリについて

AIエンジニアリング講座（AIE2026、日本語で実施）の演習・宿題用リポジトリです。講座全体を通して
「学習支援エージェント」という1つのエージェントを少しずつ育てていく構成になっています。

- 第1回：素の LLM 呼び出し（`app/ask.py`）
- 第2回：Colab で LoRA（`notebooks/lora_format_tuning.ipynb`、`scripts/make_sft_dataset.py` で用語集から SFT データを作る）
- 第3回：ツール呼び出しを追加（`app/tools.py` + `app/agent.py`）
- 第4回：評価セットのラベル付けと LLM-as-a-Judge（`tools/annotate.py` + `app/judge.py`）
- 第5回：講義資料の検索（RAG）（`app/retrieval.py` + `scripts/build_rag_index.py` + `app/agent.py --tree/--graph/--full-context`）
- 第6回：ツールを MCP サーバーの裏側に移す（`app/mcp_server.py` + MCP クライアントの `app/mcp_agent.py`）
- 第7回：Bedrock を使うチャットアプリ `simplechat/` を Terraform で AWS にデプロイする（Python の `app/` とは独立）

MCP の回は第5回から第6回に移りました。第6回の演習（`lectures/06/problem.md`）では `app.mcp_agent` を使います。
`app/agent.py --mcp` は以前の版から残っている同じ機能の経路で、docstring・コメント・`--help` には「第5回」の
表記がまだ残っていますが、MCP については第6回が正しい表記です。

コードのコメントや docstring は受講生向けに日本語で書かれています。`# TODO(第N回 演習): ...` や
`# TODO(宿題・基礎): ...` というコメントは意図的に未完成にしてある演習・宿題用のスタブです（例：`agent.py` の
`make_quiz` 登録、`mcp_server.py` の `get_lecture_summary` 公開）。指示がない限り、黙って実装を埋めたりしないでください。

## コマンド

```bash
uv sync --frozen          # 依存関係をインストール（Python 3.12、uv.lock でバージョン固定。アップグレードしない）
uv run pytest -q          # 全テストを実行（APIキー不要）
uv run pytest -q tests/test_tools.py::test_lecture_summary   # 単体テストを実行

uv run python -m app.ask "質問"                      # 第1回：ツールなしの素のLLM呼び出し
uv run python -m app.agent "質問"                     # 第3回：tools.py のツールを直接登録したエージェント
uv run python -m app.agent --trace "質問"              # ツール呼び出し・戻り値を表示
uv run python -m app.retrieval "LoRA QLoRA 違い"       # 第5回：講義資料のベクトル検索だけを実行
uv run python -m app.agent --tree --trace "質問"       # 第5回：目次（tree.json）をたどって回答（検索DB不要）
uv run python -m app.agent --graph --trace "質問"      # 第5回：検索結果からグラフ（graph.json）をたどって回答
uv run python -m app.agent --full-context "質問"       # 第5回：検索せず全資料をプロンプトに入れる（検索DB不要）
uv run python -m scripts.build_rag_index [--rebuild]  # 第5回：検索DBを作成（AIE_RAG_DB のパスに書き出す）
uv run python -m app.mcp_agent --trace "質問"          # 第6回：mcp_servers.json のサーバーのツールだけで回答
uv run python -m app.mcp_agent --list-tools           # モデルに見えるツール一覧を表示（APIキー不要）
uv run python -m app.agent --mcp --trace "質問"        # 旧経路：agent.py の指示文のままMCP経由のツールで動かす
uv run python -m app.mcp_server --http                # 用語集MCPサーバーをStreamable HTTPで起動（既定はstdio）

uv run python -m app.judge                            # 第4回：評価セットをLLMで採点し、自分のラベルと比べる
uv run python -m app.judge --model test               # APIを呼ばない規則ベースの偽モデルで採点（動作確認用）
uv run python -m app.judge --compare lectures/04/reference/labels_instructor.jsonl   # ラベル同士の一致率（APIキー不要）
uv run python -m app.judge --generate --cases data/eval/my_cases.jsonl              # 回答を app.agent で生成し直す
uv run --with streamlit==1.66.1 streamlit run tools/annotate.py                      # 第4回：ラベル付け画面

# 第7回（AWS にログイン済みで、リポジトリ直下から。詳細は simplechat/README.md）
./simplechat/scripts/setup-state-bucket.sh            # state 用 S3 バケットと terraform/backend.hcl を作る
(cd simplechat/frontend && npm ci && npm run build)   # 画面のビルド
cd simplechat/terraform && terraform init -backend-config=backend.hcl && terraform fmt -check && terraform validate
terraform plan -out=day7.tfplan                       # apply／destroy は実際の AWS リソースと料金に関わる
```

Streamlit は `uv run --with` で一時的に追加して使います。`pyproject.toml` には加えないでください。

`app.ask`／`app.agent`／`app.judge`（`--model test`・`--compare` を除く）の実行には環境変数
`GEMINI_API_KEY` が必要です。既定モデルは `gemini-3.5-flash-lite` で、環境変数 `AIE_MODEL` で
切り替えられます（503 が続くときの代替は `gemini-3.1-flash-lite`）。

ローカルでは、リポジトリ直下の `.env`（`GEMINI_API_KEY=...`、git 管理外）を uv に読み込ませて使います。
コードは `.env` を読まず、uv が `uv run` で起動するプロセスにだけ環境変数として渡します（シェル自体には
設定されません）。ターミナルを開くたびに次を実行してください。`.env` の中身は表示・読み込みしないでください。

```bash
export UV_ENV_FILE=.env                                                    # このターミナルの uv run で .env を読む
uv run python -c "import os; print(bool(os.getenv('GEMINI_API_KEY')))"    # キーの値は出さず、読めたかだけ確認（True で OK）
```

## アーキテクチャ

- `app/config.py`：`MODEL`（`AIE_MODEL`）と `GEMINI_API_KEY` の取得を一元管理しています。
  `api_error_message()` は Gemini の HTTP ステータス（429/503/4xx など）を受講生向けの日本語メッセージに
  変換する関数で、`ask.py`・`agent.py`・`judge.py` で共用しています。
- `app/tools.py`：素の Python 関数を集めたファイルで、docstring と型ヒントがそのままモデルへのツール
  説明文になります。`search_glossary` は `data/glossary.json` を読み（`@cache` でキャッシュ）、
  `get_lecture_summary` は `data/lectures/NN.md` を読みます。同じ関数が、次の2通りの方法で登録されます。
  - **第3回のパス**：`app/agent.py` が `agent.tool_plain(...)` で `pydantic_ai.Agent` に直接登録します。
  - **第6回のパス**：`app/mcp_server.py` が同じ関数を `server.tool()(...)` で MCP サーバーとして公開します。
    クライアントの `app/mcp_agent.py` は関数を直接登録せず、`app/mcp_servers.json`（Claude Desktop や
    Cursor と同じ `mcpServers` 形式。`command` なら stdio で起動、`url` なら HTTP で接続）を
    `load_mcp_servers()` で読んでツールセットを組み立てます。設定の誤りは `ConfigError` で日本語にして
    伝えます。`app/agent.py --mcp` にも同じ処理の古い版があります。このパスではツール名に `サーバー名_` の
    プレフィックスが付きます（例：`glossary_search_glossary`）。テストは `tests/test_mcp_server.py` です。
- `app/agent.py` は実行時（`build_model()`）にモデル（`GoogleModel` + `GoogleProvider`）を組み立てます。
  そのためテストは API キーなしで `agent.override(model=...)` により `TestModel` に差し替えられます。
- `app/retrieval.py`（第5回）：`data/rag_data/` の講義資料（`lectures.json`：資料→章→ページ）を
  1ページ＝1チャンクで扱います。対象資料・top-k・埋め込みモデル（`gemini-embedding-001`、768次元）などの
  定数は `app/config.py` に集約されています。検索DB は sqlite-vec の `data/rag_data/index.sqlite3`
  （第1〜3回分を同梱）で、環境変数 `AIE_RAG_DB` を設定すると作成・検索の両方がそのパスを使います。
  既定のエージェントは `search_materials` ツールで検索し、`--tree`／`--graph` は
  `agent.override(instructions=..., tools=[...])` でツールと指示を差し替え、`--full-context` は
  `run_full_context()` で全資料を一度に渡します。検索時のクエリ埋め込みにも API キーが必要です。
- `app/judge.py`（第4回）：`data/eval/rubric.md` を基準に、`data/eval/lec04_cases.jsonl` の回答を採点します。
  LLM が判定するのは grounding／scope／hint／clarity の4基準で、構造化出力（`JudgeResult`）を使い、
  理由→判定（pass/fail/unsure）の順に出力させます。末尾の「第N回」表記（`lecture_mark`）は LLM ではなく
  コードの `check_lecture_mark()` で判定します。総合判定に使う必須基準は `REQUIRED` で、clarity は
  参考扱いです。`--model test` では規則ベースの `FunctionModel` を使い、テストでも同じものを使います。
  人のラベルは `lectures/04/labels.jsonl`（受講生が作成）、講師のラベルは
  `lectures/04/reference/labels_instructor.jsonl` です。`tools/annotate.py` は `app.judge` の関数を
  再利用しています。
- データ（`data/glossary.json`、`data/lectures/NN.md`）は、エージェントが推測ではなくそこに基づいて
  回答すべき「正解データ」です。`app/ask.py` の `DEFAULT_QUESTION` は意図的に講座固有の質問にしてあります。
  第1回の素の LLM ではうまく答えられず、第3回以降のエージェントは用語集から正しく答えられる、という
  対比を見せるためです。
- `simplechat/`（第7回）：CloudFront + S3（React/Vite の画面）→ Cognito で認証 → API Gateway `POST /chat` →
  Lambda（`lambda/index.py`）→ Bedrock（既定 `us.amazon.nova-lite-v1:0`）という構成で、Terraform で
  管理します。画面用の `config.js` は Terraform が `templates/config.js.tftpl` から作って S3 に置きます。
  state は `setup-state-bucket.sh` が作る S3 バケットにあり、state・`*.tfplan`・`terraform.tfvars` は
  Git に入れません。state を削除・編集しないでください。Gemini API は使いません。

## このリポジトリ特有の決まり

- API キーは必ず環境変数 `GEMINI_API_KEY` からのみ取得します（Codespaces secret で渡す想定）。
- `pyproject.toml`／`uv.lock` の依存バージョン（pydantic-ai-slim 2.57.0、google-genai 2.31.0）は、
  講座期間中は意図的に固定しています。指示なくアップグレードしないでください。
- 各 `lectures/NN/` には `problem.md`（課題内容）と `answer.md`（受講生が記入して提出するファイル）が
  あります。`answer.md` は受講生自身が書く内容なので、丸ごと代わりに生成しないでください。
  `reference/` には講師の参考データが入っています。
- 提出は、回ごとの作業ブランチ（例：`lec01`）から自分の fork の `main` への PR で行います。宿題は
  「基礎・実装・発展」の3レベルがあり、どれか1つに取り組めば完了です。
