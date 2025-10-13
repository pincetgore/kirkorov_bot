import re
import os
from fastapi import FastAPI, Request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import asyncio
import uvicorn

# =======================
TOKEN = "8366843143:AAHYOuS-QdfpVX2KA6q9T0GW_-lx1fvioQw"
PORT = int(os.environ.get("PORT", 8000))
BASE_URL = "https://delicious-jaquelyn-pincetgorehome-cd382d55.koyeb.app"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{BASE_URL}{WEBHOOK_PATH}"
# =======================

# --- Инициализация FastAPI ---
app = FastAPI()

# --- Telegram приложение ---
telegram_app = ApplicationBuilder().token(TOKEN).build()

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == "private":
        await update.message.reply_text(
            'Здравствуйте! Пожалуйста, введите слово "да", чтобы начать.'
        )
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
        await update.message.reply_text("Хуес! Пизда!")

# --- Добавляем хэндлеры в Telegram ---
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, handle_private))
telegram_app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, handle_group))

# --- Healthcheck ---
@app.get("/")
async def healthcheck():
    return {"status": "ok"}

# --- Webhook endpoint ---
@app.post(WEBHOOK_PATH)
async def webhook(request: Request):
    json_data = await request.json()
    update = Update.de_json(json_data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"ok": True}

# --- Основной запуск ---
if __name__ == "__main__":
    asyncio.run(telegram_app.bot.set_webhook(WEBHOOK_URL))
    print(f"Webhook установлен: {WEBHOOK_URL}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
