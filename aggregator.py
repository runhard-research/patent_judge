# aggregator.py

def aggregate_chunk_results(chunk_results, threshold=0.8):
    """
    chunk_results: list of dict
      {
        "label": "対象 / 対象外",
        "confidence": float,
        "reason": str
      }
    """

    final_label = "対象"
    confidences = []
    reasons = []

    for res in chunk_results:
        confidences.append(res["confidence"])
        reasons.append(res["reason"])

        if res["label"] == "対象外":
            final_label = "対象外"

    # AND 接続なので最小 confidence を採用（保守的）
    final_confidence = min(confidences) if confidences else 0.0

    mode = "攻め" if final_confidence >= threshold else "保守"

    return {
        "final_label": final_label,
        "final_confidence": round(final_confidence, 2),
        "mode": mode,
        "detail_reasons": reasons
    }


