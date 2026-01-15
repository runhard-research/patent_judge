# ✅ 特許判定パイプライン：実行手順まとめ

## 前提ディレクトリ構成（あなたの実環境と一致）

```
patent_judge/
├── data/
│   ├── train.csv              # 学習（過去事例）
│   ├── input_unknown.csv      # 未知の特許
│   └── output_judged.csv      # 判定結果（出力）
│
├── db/
│   └── chroma/                # Vector DB（永続化）
│
├── chunking.py
├── embedder.py
├── build_vector_db.py
├── retriever.py
├── llm_chunk_judge.py
├── aggregator.py
├── pipeline.py
├── run_from_csv.py
├── test_retriever.py
├── test_llm_chunk_judge.py
├── test_aggregator.py
└── requirements.txt
```

---

## 🔰 Step 0：環境確認（最初に1回だけ）

```bash
pip install -r requirements.txt
pip show openai
```

✔ `openai` が入っている
✔ `.env` または環境変数に `OPENAI_API_KEY` がある

```bash
echo $OPENAI_API_KEY
```

---

## 🧱 Step 1：Vector DB を作る（必須・最初）

📌 **train.csv → Chroma DB に格納**

```bash
python build_vector_db.py
```

### 成功条件

```
Vector DB build completed.
Collection count: XX
Persist dir: db/chroma
```

確認：

```bash
find db/chroma -name "chroma.sqlite3"
```

✔ 見つかればOK
⚠️ ここを飛ばすと後続は全部失敗

---

## 🔎 Step 2：Retriever 単体テスト（確認用）

📌 **過去事例が正しく引けるか**

```bash
python test_retriever.py
```

### 成功例

```
=== RETRIEVE RESULT ===
判定結果: 対象
判断コメント: ...
```

✔ 類似事例が複数出る
✔ 判定結果・コメントが表示される

👉 **ここは本番では直接実行しない（確認用）**

---

## 🧠 Step 3：LLM chunk 判定テスト（OpenAI）

📌 **1 chunk を LLM に判定させる**

```bash
python test_llm_chunk_judge.py
```

### 成功例

```python
{
 'label': '対象外',
 'confidence': 0.8,
 'reason': '...'
}
```

✔ APIエラーなし
✔ JSON形式で返る

👉 **プロンプトを変えたら必ずここを再実行**

---

## ⚖ Step 4：Aggregator テスト（統合判定）

📌 **複数 chunk の結果を統合**

```bash
python test_aggregator.py
```

### 成功例

```python
{
 'final_label': '対象外',
 'final_confidence': 0.8,
 'mode': '攻め',
 'detail_reasons': [...]
}
```

✔ `攻め / 保守的` が切り替わる
✔ confidence が効いている

---

## 🚀 Step 5：本番実行（CSV → CSV）

📌 **input_unknown.csv を一括判定**

```bash
python run_from_csv.py
```

### 入力

```
data/input_unknown.csv
```

### 出力

```
data/output_judged.csv
```

中身：

```
特許番号,請求項,判定結果,confidence,モード,判断理由
JPXXXXXXX,...
```

👉 **ここが最終成果物**

---

## 🔁 プロンプト変更時の最短ループ

LLMプロンプトを変えたら：

```bash
python test_llm_chunk_judge.py
python test_aggregator.py
python run_from_csv.py
```

❌ Vector DB は作り直さない
⭕ retriever はそのまま

---

## 🧭 実行フローを1行で

```
train.csv
 → build_vector_db.py
 → test_retriever.py
 → test_llm_chunk_judge.py
 → test_aggregator.py
 → run_from_csv.py
```

---

## ✅ よくある疑問（即答）

* Q. retriever.py はいつ実行？
  → **pipeline / run_from_csv の中で自動実行**

* Q. test_*.py は本番？
  → ❌ 確認用のみ

* Q. DB作り直すタイミングは？
  → train.csv を変えたときだけ

---
