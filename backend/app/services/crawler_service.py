import requests
import trafilatura
from bs4 import BeautifulSoup
from fastapi import HTTPException


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/138.0 Safari/537.36"
    )
}


def extract_article(url: str) -> str:
    """
    Downloads a webpage and extracts clean article text.

    Strategy:
    1. Try Trafilatura.
    2. Fallback to BeautifulSoup.
    """

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=20,
        )

        response.raise_for_status()

        html = response.text

        # -----------------------------
        # First attempt: Trafilatura
        # -----------------------------

        article = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=False,
            include_links=False,
        )

        if article and len(article.strip()) > 200:
            return article.strip()

        # -----------------------------
        # Fallback: BeautifulSoup
        # -----------------------------

        soup = BeautifulSoup(html, "html.parser")

        paragraphs = soup.find_all("p")

        text = "\n".join(
            p.get_text(" ", strip=True)
            for p in paragraphs
        )

        if len(text.strip()) < 100:
            raise HTTPException(
                status_code=404,
                detail="Unable to extract meaningful article."
            )

        return text

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Crawler Error: {str(e)}"
        )