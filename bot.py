import re
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8366843143:AAHYOuS-QdfpVX2KA6q9T0GW_-lx1fvioQw"
PORT = int(os.environ.get("PORT", 8000))
BASE_URL = "https://delicious-jaquelyn-pincetgorehome-cd382d55.koyeb.app"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{BASE_URL}{WEBHOOK_PATH}"

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
        await update.message.reply_text("Хуес! Пизда!")

# --- Создаем приложение ---
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, handle_private))
app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, handle_group))

# --- Запуск через webhook ---
if __name__ == "__main__":
    # Настройка webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"{BASE_URL}/{TOKEN}"
    )
