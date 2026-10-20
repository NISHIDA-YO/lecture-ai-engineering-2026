"""第1回: 素のLLMに1回だけ質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする

ツールも会話履歴も持たない「素の」呼び出し。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse
import time

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def ask(question: str) -> tuple[str, float, int, int]:
    """質問してLLMの回答を得る。

    回答テキストに加えて、応答時間（秒）と入力/出力トークン数も返す。
    モデルや質問を変えて比較しやすいよう、main() 側で表示する。
    """
    client = genai.Client(api_key=get_api_key())

    start = time.perf_counter()
    response = client.models.generate_content(model=MODEL, contents=question)
    elapsed = time.perf_counter() - start

    usage = response.usage_metadata
    input_tokens = usage.prompt_token_count
    output_tokens = usage.candidates_token_count

    return response.text, elapsed, input_tokens, output_tokens


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    print(f"[質問] {args.question}\n")
    try:
        answer, elapsed, input_tokens, output_tokens = ask(args.question)
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)

    print(answer)
    print(f"\n[応答時間] {elapsed:.2f}秒")
    print(f"[トークン数] 入力={input_tokens} 出力={output_tokens}")


if __name__ == "__main__":
    main()
