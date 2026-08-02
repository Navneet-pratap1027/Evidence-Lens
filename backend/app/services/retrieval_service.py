from app.services.search_service import search_trusted_sources
from app.services.crawler_service import extract_article
from app.services.rag_service import chunk_text, rank_chunks


def retrieve_evidence(
    claim: str,
    top_k: int = 5,
) -> list[dict]:
    """
    Dynamic Retrieval Pipeline

    Claim
        ↓
    Tavily Search
        ↓
    Crawl Articles
        ↓
    Chunk
        ↓
    Rank
        ↓
    Return Best Evidence
    """

    search_results = search_trusted_sources(
        claim,
        max_results=top_k,
    )

    evidence = []

    for result in search_results:

        try:

            article = extract_article(result["url"])

            chunks = chunk_text(article)

            ranked_chunks = rank_chunks(
                claim,
                chunks,
                top_k=1,
            )

            if not ranked_chunks:
                continue

            best = ranked_chunks[0]

            evidence.append(
                {
                    "text": best["text"],
                    "source": result["title"],
                    "url": result["url"],
                    "reliability": 1.0,
                    "similarity": best["similarity"],
                }
            )

        except Exception:
            continue

    evidence.sort(
        key=lambda x: x["similarity"],
        reverse=True,
    )

    return evidence