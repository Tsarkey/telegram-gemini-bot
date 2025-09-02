import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import os

# 🔑 Берём ключи из переменных окружения (Render → Environment)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Debug: проверяем, что токены подтянулись
print("DEBUG TELEGRAM_TOKEN:", repr(TELEGRAM_TOKEN))
print("DEBUG GEMINI_API_KEY:", repr(GEMINI_API_KEY))

# Настраиваем Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ну привет. Чего изволишь?")

# Ответ на текстовые сообщения
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = model.generate_content(user_message)
        bot_reply = response.text
    except Exception as e:
        bot_reply = f"Ошибка: {e}"

    await update.message.reply_text(bot_reply)

def main():
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN не найден в переменных окружения")
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY не найден в переменных окружения")

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
