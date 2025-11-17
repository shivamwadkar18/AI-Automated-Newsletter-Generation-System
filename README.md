# AI-Automated-Newsletter-Generation-System
🚀 Overview

This project is an automated newsletter generator that collects real-time news, extracts article text, analyzes content, summarizes it using AI, categorizes it, scores relevance, and finally creates a beautiful HTML newsletter using professional templates.

Built with LangChain + Gemini AI + Streamlit, the system automates the entire content lifecycle:

Curate → Extract → Categorize → Score → Summarize → Generate → Preview → Download

🎯 Features

🔍 Content Curation:-
RSS feed integration
Web scraping with BeautifulSoup
Article content cleaning
Category detection (AI, Tech, Finance, Business, Sports, Health, etc.)
Deduplication + normalization


🧠 Relevance Scoring:-
Keyword match scoring
Category-weight scoring
Recency boost using publish date
Optional user-preference scoring


✍️ AI Summaries (LangChain + Gemini)
Professional, structured summaries
Bullet-point format
Tone control: professional, casual, friendly, formal
Length control: short, medium, long


🎨 Newsletter Generation
Multiple HTML templates: Default,Professional,Tech,Finance,Corporate,Minimal,Marketing
Clean section organizing
Auto CTA buttons (“Read Full Article →”)
Responsive design


🖥 Streamlit UI
Template selection
Category filter
Tone & length settings
Article count slider
Full HTML preview in app
One-click download

🏗 System Architecture
modules/

 ├── curate.py       → Collects & cleans news articles
 ├── rss_ingest.py   → Fetches RSS feeds
 ├── web_scraper.py  → Extracts article text
 ├── scoring.py      → Scores + categorizes articles
 ├── summary.py      → AI summarization (LangChain)
 ├── generator.py    → Newsletter assembly (Jinja2)
 └── utils.py        → Gemini wrapper + helpers


templates/

 ├── default.html
 ├── professional.html
 ├── tech.html
 ├── finance.html
 ├── corporate.html
 ├── minimal.html
 └── marketing.html

output/

 ├── newsletter.html
 ├── sample1_tech.html
 ├── sample2_finance.html
 ...

app.py               → Streamlit UI
main.py              → Script-based generation

📦 Installation
git clone <repo-url>
cd newsletter_project
pip install -r requirements.txt


Add your Gemini API key in .env:

GEMINI_API_KEY=your_key_here
NEWSAPI_KEY=your_newsapi_key_here   # optional

▶️ Run the UI
streamlit run app.py

📄 Output

Your newsletter is saved automatically in:
output/newsletter_ui.html
You can also download it directly from the Streamlit UI.

📚 Documentation
A complete documentation PDF is available in:
docs/curation_documentation.pdf

🧩 Use Cases
Tech newsletters
Finance briefs
AI research summaries
Marketing digest
Enterprise internal updates
Student research consolidation
