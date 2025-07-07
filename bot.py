import telebot
from dotenv import load_dotenv
import os
from gpt_handler import extract_mood_and_language
from utils import get_song_recommendations
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(
        message,
        "🎵 Hi! I'm your Mood Music Bot.\n"
        "Just tell me how you're feeling (e.g., 'I'm tired', 'need something peaceful') "
        "and I’ll recommend some songs for your mood! 🎧"
    )

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_input = message.text
    chat_id = message.chat.id

    bot.send_message(chat_id, "🔍 Detecting your mood...")

    mood, language = extract_mood_and_language(user_input)
    bot.send_message(chat_id, f"🎯 Mood: *{mood}*, 🌐 Language: *{language}*", parse_mode="Markdown")


    bot.send_message(chat_id, "🎧 Finding songs for you on Spotify...")

    songs = get_song_recommendations(mood, language)

    if not songs:
        bot.send_message(chat_id, "😔 Sorry, I couldn’t find any songs for that mood.")
        return

    for song in songs:
        title = song['title']
        artist = song['artist']
        link = song['link']
        bot.send_message(chat_id, f"🎵 *{title}* by *{artist}*\n🔗 {link}", parse_mode="Markdown")

print("✅ Bot is starting...")
bot.polling()
