# CLAUDE.md

このファイルは、このリポジトリで作業する Claude Code (claude.ai/code) にガイダンスを提供するものです。

## このリポジトリについて

AIエンジニアリング講座（AIE2026、日本語で実施）の演習・宿題用リポジトリです。講座全体を通して
「学習支援エージェント」という1つのエージェントを少しずつ育てていく構成になっています。

- 第1回：素の LLM 呼び出し（`app/ask.py`）
- 第2回：Colab で LoRA（`notebooks/lora_format_tuning.ipynb`、`scripts/make_sft_dataset.py` で用語集から SFT データを作る）
- 第3回：ツール呼び出しを追加（`app/tools.py` + `app/agent.py`）
- 第4回：評価セットのラベル付けと LLM-as-a-Judge（`tools/annotate.py` + `app/judge.py`）
- 第5回：データとコンテキストの回（まだ `lectures/05/`・`data/lectures/05.md` は存在しない）
- 第6回：ツールを MCP サーバーの裏側に移す（`app/mcp_server.py` + `app/agent.py --mcp`）

MCP の回は第5回から第6回に移りました。`app/agent.py` の docstring・コメント・`--help` と
`pyproject.toml` のコメントには「第5回」の表記がまだ残っていますが、MCP については第6回が正しい表記です。
また README は `.github/workflows/test.yml`（PR ごとのテスト）に触れていますが、このリポジトリには
存在しないため、CI に頼らずローカルで `uv run pytest -q` を実行して確認してください。

コードのコメントや docstring は受講生向けに日本語で書かれています。`# TODO(第N回 演習): ...` という
コメントは意図的に未完成にしてある演習用のスタブです（例：`agent.py` の `make_quiz` 登録、
`mcp_server.py` の `get_lecture_summary` 公開）。指示がない限り、黙って実装を埋めたりしないでください。

## コマンド

```bash
uv sync --frozen          # 依存関係をインストール（Python 3.12、uv.lock でバージョン固定。アップグレードしない）
uv run pytest -q          # 全テストを実行（APIキー不要）
uv run pytest -q tests/test_tools.py::test_lecture_summary   # 単体テストを実行

uv run python -m app.ask "質問"                      # 第1回：ツールなしの素のLLM呼び出し
uv run python -m app.agent "質問"                     # 第3回：tools.py のツールを直接登録したエージェント
uv run python -m app.agent --trace "質問"              # ツール呼び出し・戻り値を表示
uv run python -m app.agent --mcp --trace "質問"        # 第6回：同じエージェントをMCP経由のツールで動かす
uv run python -m app.agent --mcp --list-tools         # モデルに見えるツール一覧を表示（APIキー不要）
uv run python -m app.mcp_server --http                # 用語集MCPサーバーをStreamable HTTPで起動（既定はstdio）

uv run python -m app.judge                            # 第4回：評価セットをLLMで採点し、自分のラベルと比べる
uv run python -m app.judge --model test               # APIを呼ばない規則ベースの偽モデルで採点（動作確認用）
uv run python -m app.judge --compare lectures/04/reference/labels_instructor.jsonl   # ラベル同士の一致率（APIキー不要）
uv run python -m app.judge --generate --cases data/eval/my_cases.jsonl              # 回答を app.agent で生成し直す
uv run --with streamlit==1.66.1 streamlit run tools/annotate.py                      # 第4回：ラベル付け画面
```

Streamlit は `uv run --with` で一時的に追加して使います。`pyproject.toml` には加えないでください。

`app.ask`／`app.agent`／`app.judge`（`--model test`・`--compare` を除く）の実行には環境変数
`GEMINI_API_KEY` が必要です。既定モデルは `gemini-3.5-flash-lite` で、環境変数 `AIE_MODEL` で
切り替えられます（503 が続くときの代替は `gemini-3.1-flash-lite`）。

## アーキテクチャ

- `app/config.py`：`MODEL`（`AIE_MODEL`）と `GEMINI_API_KEY` の取得を一元管理しています。
  `api_error_message()` は Gemini の HTTP ステータス（429/503/4xx など）を受講生向けの日本語メッセージに
  変換する関数で、`ask.py`・`agent.py`・`judge.py` で共用しています。
- `app/tools.py`：素の Python 関数を集めたファイルで、docstring と型ヒントがそのままモデルへのツール
  説明文になります。`search_glossary` は `data/glossary.json` を読み（`@cache` でキャッシュ）、
  `get_lecture_summary` は `data/lectures/NN.md` を読みます。同じ関数が、次の2通りの方法で登録されます。
  - **第3回のパス**：`app/agent.py` が `agent.tool_plain(...)` で `pydantic_ai.Agent` に直接登録します。
  - **第6回のパス**：`app/mcp_server.py` が同じ関数を `server.tool()(...)` で MCP サーバーとして公開します。
    `app/agent.py --mcp` は `load_mcp_servers()` で `app/mcp_servers.json`（Claude Desktop や Cursor と
    同じ `mcpServers` 形式）を読み、ツールセットを組み立てます。このパスではツール名に `サーバー名_` の
    プレフィックスが付きます。
- `app/agent.py` は実行時（`build_model()`）にモデル（`GoogleModel` + `GoogleProvider`）を組み立てます。
  そのためテストは API キーなしで `agent.override(model=...)` により `TestModel` に差し替えられます。
- `app/judge.py`（第4回）：`data/eval/rubric.md` を基準に、`data/eval/lec04_cases.jsonl` の回答を採点します。
  LLM が判定するのは grounding／scope／hint／clarity の4基準で、構造化出力（`JudgeResult`）を使い、
  理由→判定（pass/fail/unsure）の順に出力させます。末尾の「第N回」表記（`lecture_mark`）は LLM ではなく
  コードの `check_lecture_mark()` で判定します。総合判定に使う必須基準は `REQUIRED` で、clarity は
  参考扱いです。`--model test` では規則ベースの `FunctionModel` を使い、テストでも同じものを使います。
  人のラベルは `lectures/04/labels.jsonl`（受講生が作成）、講師のラベルは
  `lectures/04/reference/labels_instructor.jsonl` で、採点結果は `lectures/04/judge_result.json` に
  保存されます。`--generate` は `--cases` に指定したファイルを**上書き**するため、既定の
  `data/eval/lec04_cases.jsonl` を壊さないよう必ず別ファイルを指定してください。`tools/annotate.py` は `app.judge` の関数を
  再利用しています。
- データ（`data/glossary.json`、`data/lectures/NN.md`）は、エージェントが推測ではなくそこに基づいて
  回答すべき「正解データ」です。`app/ask.py` の `DEFAULT_QUESTION` は意図的に講座固有の質問にしてあります。
  第1回の素の LLM ではうまく答えられず、第3回以降のエージェントは用語集から正しく答えられる、という
  対比を見せるためです。

## このリポジトリ特有の決まり

- API キーは必ず環境変数 `GEMINI_API_KEY` からのみ取得します（Codespaces secret で渡す想定）。
- リポジトリ直下の `.env` の中身は**決して読み込まないでください**（Read・cat・grep・source など、内容が
  出力に出る操作はすべて禁止）。読むと秘密情報がログに残るためです。存在確認（`ls`）や
  `git check-ignore` のように中身を出さない確認だけは構いません。
- `pyproject.toml`／`uv.lock` の依存バージョン（pydantic-ai-slim 2.57.0、google-genai 2.31.0）は、
  講座期間中は意図的に固定しています。指示なくアップグレードしないでください。
- 各 `lectures/NN/` には `problem.md`（課題内容）と `answer.md`（受講生が記入して提出するファイル）が
  あります。`answer.md` は受講生自身が書く内容なので、丸ごと代わりに生成しないでください。
  `reference/` には講師の参考データが入っています。
- 提出は、回ごとの作業ブランチ（例：`lec01`）から自分の fork の `main` への PR で行います。宿題は
  「基礎・実装・発展」の3レベルがあり、どれか1つに取り組めば完了です。
