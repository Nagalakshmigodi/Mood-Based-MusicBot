import telebot
from dotenv import load_dotenv
import os
from gpt_handler import extract_mood_and_language
from utils import get_song_recommendations
from keep_alive import keep_alive

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# /start and /help commands
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(
        message,
        "🎵 Hi! I'm your Mood Music Bot.\n"
        "Tell me how you're feeling (e.g., 'I'm sad, play something in Hindi') and "
        "I'll find songs that match your mood and language! 🎧"
    )

# Main handler
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_input = message.text
    chat_id = message.chat.id

    bot.send_message(chat_id, "🔍 Detecting your mood and preferred language...")

    mood, language = extract_mood_and_language(user_input)

    if mood == "default":
        bot.send_message(chat_id, "😕 Sorry, I couldn't understand your mood. Try rephrasing it.")
        return

    bot.send_message(chat_id, f"🎯 Detected mood: *{mood}*, Language: *{language}*", parse_mode="Markdown")

    bot.send_message(chat_id, "🎧 Finding songs for you on Spotify...")

    songs = get_song_recommendations(mood, language)

    if not songs:
        bot.send_message(chat_id, f"😔 No songs found for mood '{mood}' in '{language}'. Try a different input.")
        return

    for song in songs:
        title = song['title']
        artist = song['artist']
        link = song['link']
        bot.send_message(chat_id, f"🎵 *{title}* by *{artist}*\n🔗 {link}", parse_mode="Markdown")

# Start bot
print("✅ Bot is starting...")
keep_alive()
bot.polling()
