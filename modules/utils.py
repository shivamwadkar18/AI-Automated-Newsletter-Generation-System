# modules/utils.py

import os
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai

# Load API Key
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("⚠️ Warning: GEMINI_API_KEY missing in .env")

# Configure Gemini
genai.configure(api_key=API_KEY)


# ----------------------------------------------------
# Custom LLM Wrapper (replaces broken ChatGoogleGenerativeAI)
# ----------------------------------------------------
class GeminiWrapper:
    def __init__(self, model="gemini-2.5-flash", temperature=0.4):
        self.model = genai.GenerativeModel(model)
        self.temperature = temperature

    def invoke(self, prompt: str) -> str:
        """
        Drop-in replacement for LangChain llm.invoke().
        """
        response = self.model.generate_content(
            prompt,
            generation_config={"temperature": self.temperature}
        )

        return response.text.strip() if response.text else ""


# ----------------------------------------------------
# Public function used by summary.py
# ----------------------------------------------------
def get_llm():
    return GeminiWrapper()
