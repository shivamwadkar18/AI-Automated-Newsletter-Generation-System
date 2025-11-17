# modules/web_scraper.py

import requests
from bs4 import BeautifulSoup
from typing import Optional

# Strong realistic headers to avoid blocking
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml"
}


# ----------------------------------------------------------
# CLEAN HTML
# ----------------------------------------------------------
def clean_soup(soup: BeautifulSoup):
    """
    Removes noise from page so extracted text is cleaner.
    """
    for tag in soup(["script", "style", "nav", "footer", "header", "aside", "noscript"]):
        tag.decompose()
    return soup


# ----------------------------------------------------------
# EXTRACTION LOGIC WITH MULTIPLE STRATEGIES
# ----------------------------------------------------------
def extract_text_from_blocks(soup: BeautifulSoup) -> str:
    """
    Multi-stage extraction:
    1. <article>
    2. Known article containers
    3. All <p> tags fallback
    """

    # Strategy 1: <article>
    article = soup.find("article")
    if article:
        paras = article.find_all("p")
        text = "\n\n".join(p.get_text(strip=True) for p in paras if p.get_text(strip=True))
        if len(text) > 200:
            return text

    # Strategy 2: common selectors
    selectors = [
        "#content", ".post-content", ".article-body",
        ".entry-content", "#main-content", ".story-content"
    ]

    for sel in selectors:
        block = soup.select_one(sel)
        if block:
            paras = block.find_all("p")
            text = "\n\n".join(p.get_text(strip=True) for p in paras if p.get_text(strip=True))
            if len(text) > 200:
                return text

    # Strategy 3: all paragraphs
    paras = soup.find_all("p")
    text = "\n\n".join(p.get_text(strip=True) for p in paras if p.get_text(strip=True))
    return text


# ----------------------------------------------------------
# MAIN SCRAPER FUNCTION
# ----------------------------------------------------------
def fetch_article_text(url: str, timeout: int = 12) -> Optional[str]:
    """
    Fetches and extracts clean readable article text.
    """
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        r.raise_for_status()

        # Handle weird encodings safely
        r.encoding = r.apparent_encoding or "utf-8"

        soup = BeautifulSoup(r.text, "html.parser")
        soup = clean_soup(soup)

        extracted = extract_text_from_blocks(soup)
        if not extracted or len(extracted) < 80:
            return None

        # Limit to avoid bloating Gemini prompt
        return extracted[:5000]

    except Exception as e:
        print(f"Scrape failed: {url}", e)
        return None
