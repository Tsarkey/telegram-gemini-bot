import os
import logging
import google.generativeai as genai
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Логирование (будем видеть ошибки в Render логах)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Ключи из переменных окружения (Render → Environment)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    raise ValueError("Нет TELEGRAM_TOKEN или GEMINI_API_KEY в переменных окружения!")

# Настраиваем Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# Команда /start
def start(update, context):
    update.message.reply_text("Привет! Я бот на Gemini. Напиши что-нибудь.")

# Ответ на текстовые сообщения
def handle_message(update, context):
    user_message = update.message.text

    try:
        response = model.generate_content(user_message)
        bot_reply = response.text
    except Exception as e:
        bot_reply = f"Ошибка: {e}"

    update.message.reply_text(bot_reply)

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("Бот запущен...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
