import os

from dotenv import load_dotenv
from fastapi import HTTPException
from tavily import TavilyClient

load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")

if not api_key:
    raise RuntimeError("TAVILY_API_KEY not found in .env")

client = TavilyClient(api_key=api_key)


TRUSTED_DOMAINS = [
    "pib.gov.in",
    "rbi.org.in",
    "npci.org.in",
    "uidai.gov.in",
    "eci.gov.in",
    "who.int",
    "cdc.gov",
    "nih.gov",
    "un.org",
    "reuters.com",
    "apnews.com",
    "factcheck.org",
]


def search_trusted_sources(
    claim: str,
    max_results: int = 5,
) -> list[dict]:
    """
    Search trusted websites for evidence related to a claim.

    Returns:
    [
        {
            "title": "...",
            "url": "...",
            "content": "...",
            "score": 0.93
        }
    ]
    """

    try:

        response = client.search(
            query=claim,
            topic="general",
            search_depth="advanced",
            max_results=max_results,
            include_answer=False,
            include_images=False,
            include_raw_content=True,
            include_domains=TRUSTED_DOMAINS,
        )

        evidence = []

        for item in response.get("results", []):

            evidence.append(
                {
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "content": item.get("content", ""),
                    "score": round(item.get("score", 0), 3),
                }
            )

        return evidence

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Tavily Search Error: {str(e)}",
        )