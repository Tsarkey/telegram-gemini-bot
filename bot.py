import google.generativeai as genai
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

# 🔑 Берём ключи из переменных окружения (Render → Environment)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Проверим, что токены не пустые (для отладки в логах Render)
print("DEBUG TELEGRAM_TOKEN:", TELEGRAM_TOKEN)
print("DEBUG GEMINI_API_KEY:", GEMINI_API_KEY)

# Настраиваем Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")


# Команда /start
def start(update, context):
    update.message.reply_text("Ну привет. Чего изволишь?")


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
    # Создаём Updater
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Регистрируем команды и обработчики
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("Бот запущен...")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
