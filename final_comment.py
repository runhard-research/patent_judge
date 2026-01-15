from openai import OpenAI
client = OpenAI()

def generate_comment(claim, result, mode, score, details):
    detail_txt = ""
    for d in details:
        detail_txt += f"- {d['chunk_type']}: {d['chunk判定']}（{d['理由']}）\n"

    prompt = f"""
【請求項】
{claim}

【最終判定】
結果: {result}
モード: {mode}
信頼度: {score:.2f}

【根拠】
{detail_txt}

上記に基づき、特許調査報告書として自然な日本語で判断コメントを作成してください。
"""

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content

