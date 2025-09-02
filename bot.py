import os
import logging
import google.generativeai as genai
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Токены
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN не найден в переменных окружения!")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY не найден в переменных окружения!")

# Настройка Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Хэндлеры
def start(update, context):
    update.message.reply_text("Привет! Напиши что-нибудь, и я отвечу с помощью Gemini.")

def handle_message(update, context):
    user_text = update.message.text
    try:
        response = model.generate_content(user_text)
        reply = response.text if response and hasattr(response, "text") else "Не удалось получить ответ."
    except Exception as e:
        reply = f"Ошибка при запросе к Gemini: {e}"
    update.message.reply_text(reply)

# Главная функция
def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
