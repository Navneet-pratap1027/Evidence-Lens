import chromadb
from sentence_transformers import SentenceTransformer

_embedder = None
_collection = None


def _get_embedder():
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedder


def _get_collection():
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path="knowledge_base/chroma_db")
        _collection = client.get_or_create_collection("trusted_sources")
    return _collection


def retrieve_evidence(claim: str, top_k: int = 3) -> list[dict]:
    embedder = _get_embedder()
    collection = _get_collection()

    query_embedding = embedder.encode(claim).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)

    evidence = []
    for i in range(len(results["ids"][0])):
        distance = results["distances"][0][i]
        similarity = 1 - distance  # cosine distance -> similarity
        metadata = results["metadatas"][0][i]

        evidence.append({
            "text": results["documents"][0][i],
            "source": metadata.get("source", "unknown"),
            "reliability": metadata.get("reliability", 0.5),
            "similarity": round(similarity, 3),
        })

    return evidence