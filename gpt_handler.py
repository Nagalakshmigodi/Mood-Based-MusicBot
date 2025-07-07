import json
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Fallback keyword mapping
with open("mood_prompts.json", "r", encoding="utf-8") as f:
    mood_map = json.load(f)

def extract_mood_and_language(message: str):
    try:
        prompt = (
            "Extract the user's mood and language from the following message. "
            "Reply in this exact JSON format:\n"
            '{"mood": "happy", "language": "english"}\n'
            f"Message: {message}"
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful mood and language detector."},
                {"role": "user", "content": prompt}
            ]
        )

        content = response["choices"][0]["message"]["content"].strip()
        result = json.loads(content)

        mood = result.get("mood", "").lower()
        language = result.get("language", "english").lower()

        if mood in mood_map:
            return mood, language

    except Exception as e:
        print("❌ GPT fallback triggered:", e)

    # Fallback only by mood
    for mood, keywords in mood_map.items():
        if any(word.lower() in message.lower() for word in keywords):
            return mood, "english"

    return "default", "english"
