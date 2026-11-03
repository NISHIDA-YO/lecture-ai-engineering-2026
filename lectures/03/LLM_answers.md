#　第三回の演習問題の回答

## ask.pyを用いた回答

uv run python -m app.ask "AIE2026の講座の宿題にある「3レベル」とは何ですか？"
[model] gemini-3.5-flash-lite
[質問] AIE2026の講座の宿題にある「3レベル」とは何ですか？

AIE2026（AIエンジニア育成講座など）の具体的なカリキュラムテキストのお手元にないため一般的な文脈での推測になりますが、AI・プログラミング学習や生成AI活用（ChatGPTなど）の講座でよく使われる**「3レベル（3段階）」**の概念について解説します。

講座内で出される宿題や課題の「3レベル」は、おそらく以下のいずれかの分類を指している可能性が高いです。ご自身の受講内容と照らし合わせて確認してみてください。

---

### パターン1：難易度別（初級・中級・上級）

宿題の問題が、受講生のスキルに合わせて3段階の難易度に分かれているケースです。

- **レベル1（ベーシック / 必須）：**
  - **内容：** 授業の復習レベル。コードをそのまま書き写す、指示通りに基本のプロンプトを入力する、穴埋め問題など。
  - **目的：** 基本構文やツールの使い方を理解しているかの確認。
- **レベル2（スタンダード / 応用）：**
  - **内容：** 少し条件を追加する、自分で一部ロジックを考える、エラーを自力で修正するなど。
  - **目的：** 知識を「知っている」から「使える」へ引き上げる。
- **レベル3（アドバンス / 発展）：**
  - **内容：** 複数の機能を組み合わせる、効率的なコードにリファクタリングする、実務に近い複雑な課題を解決するなど。
  - **目的：** 自走力をつける、応用力を試す。

---

### パターン2：AI活用の習熟度別（プロンプト・エージェント等の段階）

生成AIやAIツールの活用法を学ぶ講座で、AIとの関わり方を3段階に分めているケースです。

- **レベル1（指示・壁打ち）：** AIに質問して答えを得る、文章を直してもらうなど、基本的な使い方。
- **レベル2（自動化・ワークフロー）：** 複数のプロンプトを組み合わせたり、APIや特定のツールを使って定型作業を自動化する。
- **レベル3（システム構築・高度な統合）：** AIエージェントを作ったり、独自のデータ（RAGなど）と連携させてカスタムアプリを構築する。

---

### パターン3：思考の深さや課題の達成度（ブルームのタソノミー等）

教育工学でよく使われる、学習の到達度を測る3つのレベルです。

- **レベル1（知識・理解）：** 学んだ内容を理解し、再現できるか。
- **レベル2（応用・分析）：** 別のシチュエーションにその知識を当てはめられるか。
- **レベル3（創造・評価）：** 自分でゼロから新しいものを生み出したり、成果物を評価・改善できるか。

---

### 💡 確実な確認方法

もし上記にピンとこない場合は、以下の方法で確認することをお勧めします。

1.  **講座のSlackやDiscord、チャット等のコミュニティで質問する：** 「今日の宿題にある『3レベル』とは、具体的にどの難易度（またはどの要件）を指していますか？」と他の受講生や講師に聞くのが一番確実です。
2.  **配布された教材（スピーチやドキュメント）の該当ページを再確認する：** 「レベル1」「レベル2」「レベル3」の定義がどこかに記載されているはずです。

[応答時間] 4.66秒
[トークン数] 入力=21 出力=790

## agetn.pyを用いた回答

uv run python -m app.agent "AIE2026の講座の宿題にある「3レベル」とは何ですか
？"
[model] gemini-3.5-flash-lite
pydantic-ai v2.57.0 • Python 3.13.16

                 agent: target • model: google:gemini-3.5-flash-lite
                   tools: 3 • capabilities: 0
      / \
     /   \       observability: off — see every model and tool call live,

/**_._**\ with cost
/ | \ set it up free with Logfire and a GitHub login:
/ | \ https://pydantic.dev/ai-setup.md
`---.._|_..---' or use any OpenTelemetry backend:
https://pydantic.dev/docs/ai/logfire/#otel

                 goes away once observability is on — or
                   PYDANTIC_AI_NO_BANNER=1

AIE2026の講座における「3レベル」とは、宿題の構成を表す3つの段階のことです。

具体的には以下の3つのレベルに分かれており、ご自身の学習状況に合わせて**どれか1つ**に取り組めば、その回の宿題は完了となります（原則として採点は行われません）。

1. **基礎**：講義内容の確認
2. **実装**：自分でコードを書く
3. **発展**：調査や試行

## --traceを追加したバージョン

uv run python -m app.agent --trace "AIE2026の講座の宿題にある「3レベル」とは
何ですか？"
[model] gemini-3.5-flash-lite
pydantic-ai v2.57.0 • Python 3.13.16

                 agent: target • model: google:gemini-3.5-flash-lite
                   tools: 3 • capabilities: 0
      / \
     /   \       observability: off — see every model and tool call live,

/**_._**\ with cost
/ | \ set it up free with Logfire and a GitHub login:
/ | \ https://pydantic.dev/ai-setup.md
`---.._|_..---' or use any OpenTelemetry backend:
https://pydantic.dev/docs/ai/logfire/#otel

                 goes away once observability is on — or
                   PYDANTIC_AI_NO_BANNER=1

AIE2026の講座における「3レベル」とは、宿題の構成を表す3つの段階のことです。

具体的には以下の3つのレベルに分かれており、**どれか1つに取り組めばその回の宿題は完了**となります（原則として採点は行いません）。

1. **基礎**：講義内容の確認
2. **実装**：自分でコードを書く
3. **発展**：調査や試行

ご自身の興味や理解度に合わせて、好きなレベルを選んで取り組んでみてくださいね。

（関連する回：第1回）

--- trace ---
[tool call] search_glossary({'query': '3レベル'})
[tool return] search_glossary -> [{"term": "宿題の3レベル", "lecture": 1, "definition": "AIE2026の宿題の構成。「基礎（講義内容の確認）」「実装（自分でコードを書く）」「発展（調査や試行）」の3段階があり、どれか1つに取り組…
[usage] RunUsage(cost=Decimal('0.0006700'), details={'text_prompt_tokens': 1025}, input_text_tokens=1025, input_tokens=1025, output_tokens=145, requests=2, tool_calls=1)

## make_quizを使って問題作成

uv run python -m app.agent --trace "第2回の内容から確認問題を1問出して"
[model] gemini-3.5-flash-lite
pydantic-ai v2.57.0 • Python 3.13.16

                 agent: target • model: google:gemini-3.5-flash-lite
                   tools: 3 • capabilities: 0
      / \
     /   \       observability: off — see every model and tool call live,

/**_._**\ with cost
/ | \ set it up free with Logfire and a GitHub login:
/ | \ https://pydantic.dev/ai-setup.md
`---.._|_..---' or use any OpenTelemetry backend:
https://pydantic.dev/docs/ai/logfire/#otel

                 goes away once observability is on — or
                   PYDANTIC_AI_NO_BANNER=1

第2回の内容から確認問題を1問出しますね！

**【問題】**
「ファインチューニング」の意味は？

（答えたいときは、自分の言葉で答えてみてくださいね！）

関係する回：第2回

--- trace ---
[tool call] make_quiz({'lecture': 2})
[tool return] make_quiz -> {"question": "「ファインチューニング」の意味は？", "answer": "事前学習済みモデルを、特定のタスクや形式に合ったデータで追加学習させること。出力の形式や口調、特定ドメインの振る舞いを身につけさせるのに向く。最新の事…
[usage] RunUsage(cost=Decimal('0.0004632'), details={'text_prompt_tokens': 994}, input_text_tokens=994, input_tokens=994, output_tokens=66, requests=2, tool_calls=1)

###　「make_quizを使って問題作成」のテストの結果
uv run pytest -q
........... [100%]
11 passed in 2.60s

## 宿題（実装）の内容

uv run python -m app.agent --trace "今日はツール呼び出しとrequestsの回数につ いて学んだ。学習ログに保存して"
[model] gemini-3.5-flash-lite
pydantic-ai v2.57.0 • Python 3.13.16

                 agent: target • model: google:gemini-3.5-flash-lite
                   output: str | DeferredToolRequests • tools: 4
      / \          capabilities: 0
     /   \

/**_._**\ observability: off — see every model and tool call live,
/ | \ with cost
/ | \ set it up free with Logfire and a GitHub login:
`---.._|_..---' https://pydantic.dev/ai-setup.md
or use any OpenTelemetry backend:
https://pydantic.dev/docs/ai/logfire/#otel

                 goes away once observability is on — or
                   PYDANTIC_AI_NO_BANNER=1

[承認待ち] save_learning_log
content: ## 本日の学び

- ツール呼び出し（Tool use / Function calling）の仕組みと使い方
- エージェントループにおける requests（API呼び出し）の回数や、コスト・レート制限への影響についての理解
  title: ツール呼び出しとrequestsの回数
  この内容で実行してよいですか？ [y/N]: y
  本日の学習内容（ツール呼び出しとrequestsの回数）を学習ログに保存しました。

ツール呼び出しやエージェントループを実装する際は、モデルとのやり取り（requests）が何回発生するかを意識することが、料金やレート制限の観点からとても重要ですね！

第3回

--- trace ---
[tool call] search*glossary({'query': 'ツール呼び出し'})
[tool return] search_glossary -> [{"term": "ツール（Tool use / Function calling）", "lecture": 3, "definition": "モデルが呼び出せるように用意した関数。モデルはツールの名前・説明・引数の型を見て、必要なと…
[tool call] save_learning_log({'content': '## 本日の学び\n- ツール呼び出し（Tool use / Function calling）の仕組みと使い方\n- エージェントループにおける requests（API呼び出し）の回数や、コスト・レート制限への影響についての理解', 'title': 'ツール呼び出しとrequestsの回数'})
[tool return] save_learning_log -> 学習の記録を保存しました: learning_log/20261103_225615*ツール呼び出しとrequestsの回数.md…
[usage] RunUsage(cost=Decimal('0.0004657'), details={'text_prompt_tokens': 994}, input_text_tokens=994, input_tokens=994, output_tokens=67, requests=1, tool_calls=1)
