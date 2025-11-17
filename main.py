# main.py

import os
from modules.curate import curate_articles
from modules.scoring import run_scoring
from modules.generator import generate_newsletter


def main():

    print("\n=== STEP 1: CURATING (RSS + NewsAPI + Scraping) ===")
    items = curate_articles()
    print(f"✓ Collected total items: {len(items)}")

    print("\n=== STEP 2: SCORING ARTICLES ===")
    scored_items = run_scoring(items, user_topics=[])
    print("✓ Scoring completed")

    print("\n=== STEP 3: GENERATING NEWSLETTER ===")

    # --------------------------------------
    # Choose template (Pick ONE)
    # Options:
    #   default
    #   professional   (Dark + Neon Green)
    #   marketing      (Orange branding)
    # --------------------------------------
    template_to_use = "professional"   # change to "marketing" or "default" anytime

    # Personalization:
    tone = "professional"      # "casual", "formal", "friendly"
    length = "short"           # "short", "medium", "long"

    try:
        html = generate_newsletter(
            scored_items,
            template_name=template_to_use,
            tone=tone,
            length=length,
            top_n=10
        )
        print("✓ Newsletter generated successfully")
    except Exception as e:
        print("\n❌ ERROR while generating newsletter:")
        print(e)
        return

    print("\n=== STEP 4: SAVING OUTPUT ===")
    outdir = "output"
    os.makedirs(outdir, exist_ok=True)

    output_path = os.path.join(outdir, "newsletter.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✓ Saved newsletter to: {output_path}")
    print("\n🎉 DONE — Your newsletter is ready!")


if __name__ == "__main__":
    main()
