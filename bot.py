import os
import re
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.environ.get("8366843143:AAHYOuS-QdfpVX2KA6q9T0GW_-lx1fvioQw")  # ← токен берётся из переменных окружения Koyeb

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

    # Проверяем, ждём ли мы "да" от пользователя
    if context.user_data.get("waiting_for_da") and re.fullmatch(r"да+", text):
        await update.message.reply_text("пизда")
        context.user_data["waiting_for_da"] = False
    elif context.user_data.get("waiting_for_da"):
        await update.message.reply_text("Попробуйте еще раз")
    elif re.fullmatch(r"да+", text):
        await update.message.reply_text("пизда")


# --- Реакция на групповые сообщения ---
async def handle_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()

    # "да", "дааа", "da", "daaa"
    if re.search(r"(да+|da+)\s*[!?,.…\s\U0001F300-\U0001FAFF]*$", text):
        await update.message.reply_text("пизда")

    # "yes" / "йес"
    elif re.search(r"(yes+|йес+|ес+)\s*[!?,.…\s\U0001F300-\U0001FAFF]*$", text):
        await update.message.reply_text("хуес! Пизда!")


# --- Запуск ---
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & filters.ChatType.PRIVATE & ~filters.COMMAND, handle_private)
    )
    app.add_handler(
        MessageHandler(filters.TEXT & filters.ChatType.GROUPS & ~filters.COMMAND, handle_group)
    )

    print("✅ Бот запущен и работает...")
    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())


if __name__ == "__main__":
    main()
