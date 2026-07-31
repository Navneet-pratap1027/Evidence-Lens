"""
One-time/manual script: populate the vector DB with trusted-source documents.
Run with: python scripts/build_knowledge_base.py
"""
import chromadb
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("all-MiniLM-L6-v2")  # free, small, fast
client = chromadb.PersistentClient(path="knowledge_base/chroma_db")
collection = client.get_or_create_collection("trusted_sources")

# Start with a handful of manually curated example documents.
# Replace/expand this with real scraped content from Reuters, WHO, PIB, etc.
documents = [
    {
        "id": "doc1",
        "text": "NPCI has not announced any ban on UPI payments in India as of 2026.",
        "source": "NPCI Official Statement",
        "reliability": 1.0,
    },
    {
        "id": "doc2",
        "text": "The World Health Organization has not issued any advisory banning a specific vaccine brand in 2026.",
        "source": "WHO",
        "reliability": 1.0,
    },
    # Add more real, sourced documents here as you build your corpus.
]

for doc in documents:
    embedding = embedder.encode(doc["text"]).tolist()
    collection.add(
        ids=[doc["id"]],
        embeddings=[embedding],
        documents=[doc["text"]],
        metadatas=[{"source": doc["source"], "reliability": doc["reliability"]}],
    )

print(f"Indexed {len(documents)} documents into the knowledge base.")