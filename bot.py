import os
import re
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# =======================
TOKEN = "8366843143:AAHYOuS-QdfpVX2KA6q9T0GW_-lx1fvioQw"
PORT = int(os.environ.get("PORT", 8000))
BASE_URL = "https://delicious-jaquelyn-pincetgorehome-cd382d55.koyeb.app"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{BASE_URL}{WEBHOOK_PATH}"
# =======================

# --- Telegram приложение ---
telegram_app = ApplicationBuilder().token(TOKEN).build()

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == "private":
        await update.message.reply_text(
            'Здравствуйте! Пожалуйста, введите слово "да", чтобы начать.'
        )
        context.user_data["waiting_for_da"] = True

# Личные сообщения
async def handle_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()
    if context.user_data.get("waiting_for_da") and re.fullmatch(r"да+", text, re.IGNORECASE):
        await update.message.reply_text("пизда")
        context.user_data["waiting_for_da"] = False
    elif context.user_data.get("waiting_for_da"):
        await update.message.reply_text("Попробуйте еще раз")
    elif re.fullmatch(r"да+", text, re.IGNORECASE):
        await update.message.reply_text("пизда")

# Групповые сообщения
async def handle_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()
    if re.search(r"\b(да+|da+)\b\s*[!?,.…\s\U0001F300-\U0001FAFF]*$", text, re.IGNORECASE):
        await update.message.reply_text("пизда")
    elif re.search(r"(ye+s+|йе+с+|е+с+)\s*[!?,.…\s\U0001F300-\U0001FAFF]*$", text, re.IGNORECASE):
        await update.message.reply_text("Хуес! Пизда!")

# Добавляем обработчики
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, handle_private))
telegram_app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, handle_group))

# --- Flask сервер ---
app = Flask(__name__)

# Health check для UptimeRobot
@app.route("/", methods=["GET"])
def health():
    return "OK", 200

# Webhook для Telegram
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)
        if not data:
            return "No JSON", 400
        update = Update.de_json(data, telegram_app.bot)
        # Создаём задачу для async обработчиков
        asyncio.get_event_loop().create_task(telegram_app.process_update(update))
        return "OK", 200
    except Exception as e:
        print("Webhook error:", e)
        return "Error", 500

# --- Запуск ---
if __name__ == "__main__":
    from waitress import serve

    async def main():
        # Устанавливаем webhook
        await telegram_app.bot.set_webhook(WEBHOOK_URL)
        print(f"✅ Webhook установлен: {WEBHOOK_URL}")

        # Запуск Flask через Waitress
        serve(app, host="0.0.0.0", port=PORT)

    asyncio.run(main())
