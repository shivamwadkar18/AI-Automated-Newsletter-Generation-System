# app.py
import streamlit as st
import os
from modules.curate import curate_articles
from modules.scoring import run_scoring
from modules.generator import generate_newsletter


# -----------------------------------------------------
# Streamlit Page Config
# -----------------------------------------------------
st.set_page_config(
    page_title="AI Newsletter Generator",
    page_icon="📰",
    layout="wide",
)


# -----------------------------------------------------
# Sidebar Controls
# -----------------------------------------------------
st.sidebar.title("⚙️ Settings")

template = st.sidebar.selectbox(
    "Select Template",
    ["default", "professional", "marketing", "clean", "tech", "finance", "corporate", "minimal"]
)

tone = st.sidebar.selectbox(
    "Writing Tone",
    ["professional", "casual", "friendly", "formal"]
)

length = st.sidebar.selectbox(
    "Summary Length",
    ["short", "medium", "long"]
)

# ⭐ NEW — Category Selector
selected_category = st.sidebar.selectbox(
    "Select News Category",
    ["All", "Tech", "Finance", "Business", "Health", "Sports", "AI"]
)

top_n = st.sidebar.slider(
    "Number of Articles",
    5, 20, 10
)

generate_btn = st.sidebar.button("🚀 Generate Newsletter")


# -----------------------------------------------------
# Main Page Header
# -----------------------------------------------------
st.title("📰 AI-Powered Newsletter Generator")
st.write("Generate professional newsletters in seconds using AI.")


# -----------------------------------------------------
# Trigger Only When Button Is Clicked
# -----------------------------------------------------
if generate_btn:

    with st.spinner("Collecting and processing articles..."):

        # Step 1 – Curate
        items = curate_articles()

        # Step 2 – Score
        scored_items = run_scoring(items)

        # ⭐ NEW — Apply category filter
        if selected_category != "All":
            scored_items = [a for a in scored_items if a.get("category") == selected_category]

        # If nothing matches, show message
        if len(scored_items) == 0:
            st.error(f"No articles found for category: {selected_category}")
            st.stop()

        # Step 3 – Generate Newsletter
        html = generate_newsletter(
            scored_items,
            template_name=template,
            tone=tone,
            length=length,
            top_n=top_n
        )

        # Save a copy to output folder
        os.makedirs("output", exist_ok=True)
        with open("output/newsletter_ui.html", "w", encoding="utf-8") as f:
            f.write(html)

    st.success("Newsletter generated successfully!")

    # -------------------------------------------------
    # Preview Newsletter
    # -------------------------------------------------
    st.subheader("📄 Newsletter Preview")
    st.components.v1.html(html, height=900, scrolling=True)

    # -------------------------------------------------
    # Download Button
    # -------------------------------------------------
    st.download_button(
        label="📥 Download Newsletter HTML",
        data=html,
        file_name="newsletter.html",
        mime="text/html"
    )

else:
    st.info("Use the sidebar to configure settings and click **Generate Newsletter**.")
