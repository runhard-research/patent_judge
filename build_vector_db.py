# build_vector_db.py
import pandas as pd
import chromadb
from chunking import chunk_claim
from embedder import get_embedder

PERSIST_DIR = "db/chroma"
COLLECTION_NAME = "patent_chunks"

df = pd.read_csv("data/train.csv")
model = get_embedder()

# ★★★ ここが最大の変更点 ★★★
client = chromadb.PersistentClient(
    path=PERSIST_DIR
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)

doc_id = 0
for _, row in df.iterrows():
    chunks = chunk_claim(str(row["請求項"]))
    for c in chunks:
        emb = model.encode(c["text"]).tolist()
        collection.add(
            ids=[str(doc_id)],
            embeddings=[emb],
            documents=[c["text"]],
            metadatas=[{
                "chunk_type": c["type"],
                "判定結果": row["判定結果"],
                "判断コメント": row["判断コメント"]
            }]
        )
        doc_id += 1

print("Vector DB build completed.")
print("Collection count:", collection.count())
print("Persist dir:", PERSIST_DIR)






