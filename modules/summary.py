# modules/summary.py

from modules.utils import get_llm

def summarize_article(title, content, tone="professional", length="short"):
    """
    Direct Gemini summarization without LangChain.
    Avoids all 'models' attribute errors.
    """

    llm = get_llm()

    length_map = {
        "short": "Write 3 bullet points.",
        "medium": "Write 5 concise bullet points.",
        "long": "Write 7 detailed bullet points."
    }

    prompt = f"""
You are an expert newsletter writer.

Write a summary in a {tone} tone.
{length_map.get(length, "Write 3 bullet points.")}

Title: {title}

Content:
{content[:3000]}

Format:
- Bullet points ONLY
- No intro text
- No conclusion
"""

    return llm.invoke(prompt)