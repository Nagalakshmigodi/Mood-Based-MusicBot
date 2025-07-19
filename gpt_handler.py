import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load mood prompts mapping
with open("mood_prompts.json", "r", encoding="utf-8") as f:
    mood_map = json.load(f)

def extract_mood_and_language(message: str):
    try:
        system_prompt = (
            "You are a multilingual music recommendation assistant. "
            "Extract the user's mood and the language they want the music in. "
            "Support all major global languages including Spanish, French, Korean, Japanese, Arabic, and Indian languages."
        )

        user_prompt = f"""
Only reply in this exact JSON format:
{{
  "mood": "<mood>",
  "language": "<language>"
}}

Examples:
Input: "I'm feeling energetic, give me Spanish songs"
Output: {{"mood": "energetic", "language": "spanish"}}

Input: "Feeling low today, something soothing in Korean please"
Output: {{"mood": "sad", "language": "korean"}}

Input: "Play something relaxing in French"
Output: {{"mood": "relaxed", "language": "french"}}

Now extract mood and language from:
"{message}"
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        content = response.choices[0].message.content.strip()
        result = json.loads(content)

        mood = result.get("mood", "").lower()
        language = result.get("language", "english").lower()

        if mood in mood_map:
            return mood, language

    except Exception as e:
        print("❌ GPT fallback triggered:", e)

    # Fallback: keyword-based detection
    for mood, keywords in mood_map.items():
        if any(word.lower() in message.lower() for word in keywords):
            for lang in ["english", "hindi", "telugu", "tamil", "punjabi", "kannada", "malayalam",
                         "spanish", "french", "german", "korean", "japanese", "arabic"]:
                if lang in message.lower():
                    return mood, lang
            return mood, "english"

    return "default", "english"
