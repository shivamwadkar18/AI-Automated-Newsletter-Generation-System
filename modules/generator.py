# modules/generator.py
from jinja2 import Environment, FileSystemLoader
from modules.summary import summarize_article


def generate_newsletter(
        items,
        template_name="professional",     # default is your new UI
        tone="professional",
        length="short",
        top_n=8
    ):
    """
    Generates a complete HTML newsletter with:
    - Category-based sections
    - Personalized tone & summary length
    - Supports rss_url + scraped_url
    - Professional templates
    """

    # Load templates folder
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template(f"{template_name}.html")

    # Select top-N by score (handled in scoring later)
    selected = sorted(items, key=lambda x: x.get("score", 0), reverse=True)[:top_n]

    # Group by category
    sections = {}
    for article in selected:
        category = article.get("category", "General")

        if category not in sections:
            sections[category] = []

        # generate personalized summary
        summary = summarize_article(
            title=article.get("title", ""),
            content=article.get("content", ""),
            tone=tone,
            length=length
        )

        # URL method C → rss_url OR scraped_url
        url = article.get("rss_url") or article.get("scraped_url") or "#"

        sections[category].append({
            "title": article.get("title"),
            "summary": summary,
            "url": url,
            "cta": "Read Full Article →"
        })

    # Render final HTML template
    html = template.render(
        sections=sections,
        newsletter_title="AI-Powered Daily Newsletter",
        tone=tone,
        length=length,
        manage_link="#"  # placeholder link for settings
    )

    return html
