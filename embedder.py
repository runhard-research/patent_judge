from sentence_transformers import SentenceTransformer

_model = None

def get_embedder():
    global _model
    if _model is None:
        _model = SentenceTransformer("nomic-ai/nomic-embed-text-v1",trust_remote_code=True)
    return _model

