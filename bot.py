import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import re

TOKEN = "8366843143:AAHYOuS-QdfpVX2KA6q9T0GW_-lx1fvioQw"

# --- Реакция на /start в личных сообщениях ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == "private":
        await update.message.reply_text('Пожалуйста, введите слово "да", чтобы начать')
        context.user_data["waiting_for_da"] = True


# --- Реакция на личные сообщения ---
async def handle_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()

    # Проверяем, ждём ли мы "да"
    if context.user_data.get("waiting_for_da"):
        if re.fullmatch(r"д+а+", text, re.IGNORECASE):
            await update.message.reply_text("пизда")
            context.user_data["waiting_for_da"] = False
        else:
            await update.message.reply_text("Попробуйте ещё раз")


# --- Реакция на групповые сообщения ---
async def handle_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()

    # если сообщение заканчивается на "да" или "da"
    if re.search(r"\b(д+а+|d+a+)+\s*(?:[!?,.…\s\U0001F300-\U0001FAFF]*)$", text, re.IGNORECASE):
        await update.message.reply_text("пизда")

    # если сообщение содержит "yes" или "йес"
    elif re.search(r"\b(y+e+s+|е+с+|й+е+с+)+\s*(?:[!?,.…\s\U0001F300-\U0001FAFF]*)$", text, re.IGNORECASE):
        await update.message.reply_text("хуес")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # --- /start ---
    app.add_handler(CommandHandler("start", start))

    # --- личные сообщения ---
    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.ChatType.PRIVATE & ~filters.COMMAND,
            handle_private,
        )
    )

    # --- групповые чаты ---
    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.ChatType.GROUPS & ~filters.COMMAND,
            handle_group,
        )
    )

    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()