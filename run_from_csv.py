# run_from_csv.py
import pandas as pd
from pipeline import judge_one_claim

INPUT_CSV = "data/input_unknown.csv"
OUTPUT_CSV = "data/output_judged.csv"

df = pd.read_csv(INPUT_CSV)

results = []

for _, row in df.iterrows():
    claim_text = str(row["請求項"])
    result = judge_one_claim(claim_text)

    results.append({
        "特許番号": row.get("特許番号", ""),
        "請求項": claim_text,
        "判定結果": result["final_label"],
        "confidence": result["final_confidence"],
        "モード": result["mode"],
        "判断理由": " / ".join(result["detail_reasons"])
    })

out_df = pd.DataFrame(results)
out_df.to_csv(OUTPUT_CSV, index=False)

print(f"Judgement completed: {OUTPUT_CSV}")

