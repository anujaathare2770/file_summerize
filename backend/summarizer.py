import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-flash-latest")

def summarize(text: str) -> str:
    try:
        prompt = f"""
Summarize this text.

FORMAT RULES:
- Use UPPERCASE headings
- Use • for bullet points
- Do NOT use *, -, or markdown symbols

TEXT:
{text[:8000]}
"""
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Gemini Error: {str(e)}"
