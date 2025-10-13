import re
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from flask import Flask, request

TOKEN = "8366843143:AAHYOuS-QdfpVX2KA6q9T0GW_-lx1fvioQw"
WEBHOOK_URL = "https://delicious-jaquelyn-pincetgorehome-cd382d55.koyeb.app"

# --- Telegram обработчики ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == "private":
        await update.message.reply_text('Пожалуйста, введите слово "да", чтобы начать')
        context.user_data["waiting_for_da"] = True


async def handle_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()
    if context.user_data.get("waiting_for_da") and re.fullmatch(r"да+", text, re.IGNORECASE):
        await update.message.reply_text("пизда")
        context.user_data["waiting_for_da"] = False
    elif context.user_data.get("waiting_for_da"):
        await update.message.reply_text("Попробуйте еще раз")
    elif re.fullmatch(r"да+", text, re.IGNORECASE):
        await update.message.reply_text("пизда")


async def handle_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()
    if re.search(r"\b(да+|da+)\b\s*[!?,.…\s\U0001F300-\U0001FAFF]*$", text, re.IGNORECASE):
        await update.message.reply_text("пизда")
    elif re.search(r"(ye+s+|йе+с+|е+с+)\s*[!?,.…\s\U0001F300-\U0001FAFF]*$", text, re.IGNORECASE):
        await update.message.reply_text("Хуес")


# --- Flask сервер для webhook и healthcheck ---
app = Flask(__name__)
telegram_app = ApplicationBuilder().token(TOKEN).build()

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, handle_private))
telegram_app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, handle_group))

@app.route("/", methods=["GET"])
def health():
    return "OK", 200

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    await telegram_app.process_update(update)
    return "OK", 200


if __name__ == "__main__":
    import asyncio

    async def main():
        # Устанавливаем webhook при запуске
        await telegram_app.bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")
        print("✅ Webhook установлен!")
        from waitress import serve
        serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

    asyncio.run(main())
