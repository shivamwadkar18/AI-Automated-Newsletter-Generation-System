from typing import List, Dict
from datetime import datetime

# ----------------------------
# Category Keyword Map
# ----------------------------
CATEGORY_KEYWORDS = {
    "AI": [
        "ai", "artificial intelligence", "machine learning", "deep learning",
        "neural network", "openai", "google ai", "chatgpt", "llm", "model"
    ],
    "Tech": [
        "tech", "software", "hardware", "cloud", "startup", "developer",
        "programming", "gadgets", "technology"
    ],
    "Finance": [
        "stock", "market", "finance", "economy", "investment", "earnings",
        "crypto", "bitcoin", "inflation", "recession"
    ],
    "Business": [
        "acquisition", "merger", "company", "business", "corporate", "startup funding"
    ],
    "Sports": [
        "football", "cricket", "match", "tournament", "fifa", "goal"
    ],
    "Health": [
        "health", "medical", "vaccine", "covid", "disease", "study"
    ]
}


# ----------------------------
# Detect Category
# ----------------------------
def detect_category(item):
    text = (item.get("title", "") + " " + item.get("content", "")).lower()

    for cat, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return cat

    return "General"


# ----------------------------
# Compute Score
# ----------------------------
def compute_simple_score(item: Dict, user_topics: List[str] = None) -> float:

    # auto-category detection
    item["category"] = detect_category(item)

    text = (item.get("title", "") + " " + item.get("content", "")).lower()
    score = 0.0

    # category keyword scoring
    for cat, kw_list in CATEGORY_KEYWORDS.items():
        for kw in kw_list:
            if kw in text:
                score += 1.0

    # recency boost
    pub = item.get("published")
    if pub:
        try:
            if hasattr(pub, "tzinfo") and pub.tzinfo:
                pub = pub.replace(tzinfo=None)
            age_days = (datetime.utcnow() - pub).days
            recency_factor = max(0.0, 1.0 - (age_days / 30.0))
            score += recency_factor * 2.0
        except:
            pass

    return round(score, 3)


# ----------------------------
# Main Scoring Function
# ----------------------------
def run_scoring(items: List[Dict], user_topics: List[str] = None) -> List[Dict]:
    for it in items:
        it["score"] = compute_simple_score(it, user_topics)

    items.sort(key=lambda x: x.get("score", 0), reverse=True)
    return items
