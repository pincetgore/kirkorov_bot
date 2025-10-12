import re
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "8366843143:AAHYOuS-QdfpVX2KA6q9T0GW_-lx1fvioQw"

# --- Реакция на /start в личных сообщениях ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == "private":
        await update.message.reply_text(
            'Здравствуйте! Пожалуйста, введите слово "да", чтобы начать.'
        )
        context.user_data["waiting_for_da"] = True

# --- Реакция на личные сообщения ---
async def handle_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()

    if context.user_data.get("waiting_for_da") and re.fullmatch(r"да+", text, re.IGNORECASE):
        await update.message.reply_text("пизда")
        context.user_data["waiting_for_da"] = False
    elif context.user_data.get("waiting_for_da"):
        await update.message.reply_text("Попробуйте еще раз")
    elif re.fullmatch(r"да+", text, re.IGNORECASE):
        await update.message.reply_text("пизда")

# --- Реакция на групповые сообщения ---
async def handle_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()

    if re.search(r"(да+|da+)\s*[!?,.…\s\U0001F300-\U0001FAFF]*$", text, re.IGNORECASE):
        await update.message.reply_text("пизда")

    elif re.search(r"(ye+s+|йе+с+|е+с+)\s*[!?,.…\s\U0001F300-\U0001FAFF]*$", text, re.IGNORECASE):
        await update.message.reply_text("хуес")

# --- Запуск ---
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, handle_private))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, handle_group))

    print("Бот запущен...")
    app.run_polling()
