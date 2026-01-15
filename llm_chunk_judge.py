# llm_chunk_judge.py
import json
from openai import OpenAI

client = OpenAI()

MODEL_NAME = "gpt-4o-mini"  # 軽量・安定。必要なら変更可


def format_similar_chunks(similar_chunks, max_items=5):
    """
    retriever の結果を LLM 用テキストに整形
    """
    lines = []
    for i, item in enumerate(similar_chunks[:max_items], 1):
        meta = item["metadata"]
        lines.append(
            f"[類似事例{i}]\n"
            f"判定結果: {meta['判定結果']}\n"
            f"判断コメント: {meta['判断コメント']}"
        )
    return "\n\n".join(lines)


def judge_chunk(chunk_text, similar_chunks):
    """
    1 chunk を LLM で判定する
    戻り値: dict {label, confidence, reason}
    """

    similar_text = format_similar_chunks(similar_chunks)

    prompt = f"""
あなたは企業の知財部に所属する特許評価の専門家です。
以下の「請求項の一部（chunk）」が、
当社の開発案件の技術範囲に該当するかを判断してください。

【評価ルール】
- 独立請求項は AND 接続であり、要件を満たさない構成があれば「対象外」とする
- 文頭の「〇〇について」「〇〇に関する」は技術分野把握に使う
- 文中の「〇〇を有する」「〇〇を備える」は構成要件として重視する
- 文末が単なるハード名称・装置名称の場合、非該当理由になり得る
- 類似事例の判断コメントを参考にしてよいが、必ず自分で判断すること

【重要】
「自然言語処理モデル」「機械学習モデル」「AIモデル」
などが明示的に記載されている場合、
構成が抽象的であっても当社技術との関連性が
ある可能性を考慮して判定すること。

【未知の請求項 chunk】
{chunk_text}

【類似事例】
{similar_text}

【出力形式（必ずJSON）】
{{
  "label": "対象 または 対象外",
  "confidence": 0.0〜1.0,
  "reason": "判断理由を簡潔に記載"
}}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a patent analysis expert."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        response_format={"type": "json_object"}
    )

    content = response.choices[0].message.content
    return json.loads(content)



