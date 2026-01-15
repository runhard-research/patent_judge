# retriever.py
import chromadb
from embedder import get_embedder

PERSIST_DIR = "db/chroma"
COLLECTION_NAME = "patent_chunks"

class ChunkRetriever:
    def __init__(self, top_k=5):
        self.client = chromadb.PersistentClient(path=PERSIST_DIR)
        self.collection = self.client.get_collection(COLLECTION_NAME)
        self.model = get_embedder()
        self.top_k = top_k

    def retrieve(self, chunk_text):
        query_emb = self.model.encode(chunk_text).tolist()
        results = self.collection.query(
            query_embeddings=[query_emb],
            n_results=self.top_k
        )

        hits = []
        for i in range(len(results["documents"][0])):
            hits.append({
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i]
            })
        return hits


