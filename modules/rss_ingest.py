# modules/rss_ingest.py
import feedparser
from typing import List, Dict
from datetime import datetime


def fetch_rss_feed(feed_url: str, max_items: int = 10) -> List[Dict]:
    """
    Fetch a single RSS feed and return normalized items:
    {
        title, link, published, summary, content, category
    }
    """
    d = feedparser.parse(feed_url)
    items = []

    for entry in d.entries[:max_items]:

        # --- Published Time ---
        try:
            published = datetime(*entry.published_parsed[:6])
        except:
            published = None

        # --- Category ---
        category = None
        if "tags" in entry and entry.tags:
            try:
                category = entry.tags[0].get("term")
            except:
                category = None

        # --- Content ---
        content = ""
        if "content" in entry and entry.content:
            content = entry.content[0].get("value", "")
        else:
            content = (
                entry.get("summary", "")
                or entry.get("description", "")
                or ""
            )

        # --- Summary ---
        summary = (
            entry.get("summary", "")
            or entry.get("description", "")
            or content[:200]
        )

        # --- Build item ---
        items.append({
            "title": entry.get("title", "No Title"),
            "link": entry.get("link", ""),
            "rss_url": entry.get("link", ""),      # required for generator
            "published": published,
            "summary": summary,
            "content": content,
            "category": category or "General",
            "score": 0.0   # scoring module will update this later
        })

    return items


def fetch_multiple_feeds(feed_list: List[str]) -> List[Dict]:
    """
    Fetches multiple RSS feeds and returns a combined list of items.
    """
    all_items = []
    for f in feed_list:
        try:
            all_items.extend(fetch_rss_feed(f, max_items=8))
        except Exception as e:
            print(f"[RSS ERROR] Could not fetch {f}: {e}")
    return all_items
