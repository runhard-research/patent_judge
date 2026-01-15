# pipeline.py
from chunking import chunk_claim
from retriever import ChunkRetriever
from llm_chunk_judge import judge_chunk
from aggregator import aggregate_chunk_results


def judge_one_claim(claim_text):
    retriever = ChunkRetriever()
    chunks = chunk_claim(claim_text)

    chunk_results = []

    for c in chunks:
        similar = retriever.retrieve(c["text"])
        result = judge_chunk(c["text"], similar)
        chunk_results.append(result)

    final = aggregate_chunk_results(chunk_results)

    return final

