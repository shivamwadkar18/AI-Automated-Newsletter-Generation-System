# modules/curate.py
import os
import requests
from typing import List, Dict, Set
from datetime import datetime

from modules.rss_ingest import fetch_multiple_feeds
from modules.web_scraper import fetch_article_text


# -------------------------------
# Load NewsAPI Key
# -------------------------------
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

if not NEWSAPI_KEY:
    print("Warning: NEWSAPI_KEY not found in .env — NewsAPI headlines will be skipped.")


# -------------------------------
# Default RSS Feeds
# -------------------------------
DEFAULT_FEEDS = [
    "https://arstechnica.com/feed/",            # Reliable tech news
    "https://www.wired.com/feed/rss",           # Wired tech feed
    "https://www.theverge.com/rss/index.xml",   # Keep Verge (works fine)
    "https://feeds.finance.yahoo.com/rss/2.0/headline?s=yhoo&region=US&lang=en-US"  # Finance
]


# -------------------------------
# Fetch from NewsAPI
# -------------------------------
def fetch_newsapi_headlines(country="us", page_size=10) -> List[Dict]:
    if not NEWSAPI_KEY:
        return []

    try:
        url = (
            "https://newsapi.org/v2/top-headlines"
            f"?country={country}&pageSize={page_size}&apiKey={NEWSAPI_KEY}"
        )

        res = requests.get(url, timeout=8)
        res.raise_for_status()
        data = res.json()

        output = []
        for art in data.get("articles", []):
            output.append({
                "title": art.get("title"),
                "link": art.get("url"),
                "published": art.get("publishedAt"),
                "summary": art.get("description") or "",
            })

        return output

    except Exception as e:
        print("NewsAPI fetch error:", e)
        return []


# -------------------------------
# Main Curation Pipeline
# -------------------------------
def curate_articles(
    feeds: List[str] = None,
    max_items: int = 30
) -> List[Dict]:
    """
    Returns curated list of articles:

    {
        title: str,
        rss_url: str,
        scraped_url: str,
        published: str,
        summary: str,
        content: str,
        category: str,
        score: float
    }
    """

    feeds = feeds or DEFAULT_FEEDS
    collected: List[Dict] = []

    # 1. RSS Feeds
    collected.extend(fetch_multiple_feeds(feeds))

    # 2. NewsAPI
    collected.extend(fetch_newsapi_headlines())

    # ----------------------------------
    # Deduplicate by link or title
    # ----------------------------------
    seen: Set[str] = set()
    cleaned: List[Dict] = []

    for item in collected:
        link = item.get("link") or ""
        title = item.get("title") or ""

        key = link if link else title[:100]

        if key in seen:
            continue

        seen.add(key)
        cleaned.append(item)

        if len(cleaned) >= max_items:
            break

    # ----------------------------------
    # Scrape full content & add URLs
    # ----------------------------------
    for item in cleaned:
        link = item.get("link")

        # RSS URL always stored
        item["rss_url"] = link

        # Scrape article text
        text = None
        if link:
            try:
                text = fetch_article_text(link)
            except Exception as e:
                print(f"Scrape failed: {link}", e)

        item["content"] = text or item.get("summary") or ""

        # fallback title
        if not item.get("title"):
            item["title"] = item["content"][:60] + "..."

        # scraped_url is same as link for now (can change later)
        item["scraped_url"] = link

        # Placeholders
        item["category"] = "Uncategorized"
        item["score"] = 0.0

    return cleaned
