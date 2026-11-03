# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：
  - 質問「AIE2026の講座の宿題にある「3レベル」とは何ですか？」
  - 第1回（`app.ask`）：講座の情報を持っていないため、「難易度別」「AI活用の習熟度別」「ブルームのタキソノミー」など一般論の推測を3パターン並べ、「講座のSlackで確認を」と締めくくった（出力790トークン）。どれも正解ではない。
  - エージェント（`app.agent`）：用語集を検索し、「基礎（講義内容の確認）・実装（自分でコードを書く）・発展（調査や試行）の3段階で、どれか1つに取り組めば完了（原則採点なし）」と、`glossary.json` の内容どおり簡潔に正しく回答した。最後に「関連する回：第1回」も示した。
- `--trace` で見えたツール呼び出し（ツール名と引数）：
  - `search_glossary({'query': '3レベル'})` → 用語「宿題の3レベル」（第1回）の定義が返った
- 1つの質問での LLM 呼び出し回数（`requests`）：
  - `requests=2`（`tool_calls=1`）。1回目でモデルがツール呼び出しを決め、2回目でツールの戻り値をもとに回答を生成している
- 追加したツールと、docstring に書いた説明：
  - ツール：`make_quiz(lecture: int) -> str`（指定した回の用語を `random.choice` で1つ選び、`{"question": "「○○」の意味は？", "answer": 定義}` を JSON で返す。用語がない回は「第N回の用語は用語集にありません」と返す）
  - docstring：「指定した回の用語集から確認問題を1問作って返す。『第2回の確認問題を出して』のように確認問題やクイズを求められたときに使う。question を出題し、answer は答え合わせに使う（先に見せない）」
  - 結果：「第2回の内容から確認問題を1問出して」で `make_quiz({'lecture': 2})` が呼ばれ、「「ファインチューニング」の意味は？」と答えを伏せて出題された（`requests=2`, `tool_calls=1`）。`uv run pytest -q` は 11 passed。

## 宿題

（回答の詳細はLLM_answers.mdに記載）

- 取り組んだレベル：実装
- やったこと：
  - `app/tools.py` に `save_learning_log(title, content)` を追加。学習の記録を `learning_log/日時_見出し.md` に Markdown で保存する（見出し・本文が空なら保存しない）
  - `app/agent.py` で `requires_approval=True` を付けて登録し、`output_type=[str, DeferredToolRequests]` に変更
  - CLI に承認フローを追加：承認待ち（`DeferredToolRequests`）になったら引数を表示して `[y/N]` で確認し、`DeferredToolResults` と `message_history` を渡して再実行（拒否時は `ToolDenied` を返す）
  - `INSTRUCTIONS` に「学習の記録を残すよう頼まれたら save_learning_log で保存する」を追加。APIを使わない TestModel のテストも追加（全15件 passed）
- 結果：
  - 「今日はツール呼び出しとrequestsの回数について学んだ。学習ログに保存して」と質問
  - trace：`search_glossary({'query': 'ツール呼び出し'})` → `save_learning_log({'title': 'ツール呼び出しとrequestsの回数', 'content': '## 本日の学び ...'})`
  - 保存前に `[承認待ち] save_learning_log` と title・content が表示されて実行が止まり、`y` と答えると `learning_log/20261103_225615_ツール呼び出しとrequestsの回数.md` が作られた
- 気づき・疑問：
  - ツールの docstring の書き方が意外と難しい。モデルは docstring だけを見て「いつ使うか」「どんな引数を渡すか」を判断するため、使う場面（「記録を求められたときだけ使う」）や引数の中身まで具体的に書く必要があった
  - 一方で、承認付きツールの実装は意外とシンプルだった。`requires_approval=True` を付けて、承認結果を渡して再実行するループを書くだけで、取り消しにくい操作の前に人の確認を挟める
