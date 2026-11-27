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

- 取り組んだレベル：基礎 / 実装 / 発展
- やったこと：
- 結果：
- 気づき・疑問：
