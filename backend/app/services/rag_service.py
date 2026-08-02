from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

_embedder = None


def get_embedder():
    """
    Load embedding model only once.
    """
    global _embedder

    if _embedder is None:
        _embedder = SentenceTransformer("all-MiniLM-L6-v2")

    return _embedder


def chunk_text(
    text: str,
    chunk_size: int = 300,
    overlap: int = 50,
) -> list[str]:
    """
    Split long article into overlapping chunks.
    """

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def rank_chunks(
    claim: str,
    chunks: list[str],
    top_k: int = 3,
) -> list[dict]:
    """
    Rank article chunks according to similarity with the claim.
    """

    embedder = get_embedder()

    claim_embedding = embedder.encode([claim])

    chunk_embeddings = embedder.encode(chunks)

    similarities = cosine_similarity(
        claim_embedding,
        chunk_embeddings,
    )[0]

    ranked = []

    for chunk, score in zip(chunks, similarities):
        ranked.append(
            {
                "text": chunk,
                "similarity": round(float(score), 3),
            }
        )

    ranked.sort(
        key=lambda x: x["similarity"],
        reverse=True,
    )

    return ranked[:top_k]