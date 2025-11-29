import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiohttp import web

# Получаем токен
TOKEN = os.getenv("BOT_TOKEN")
# Получаем порт от Koyeb, или используем 8000 по умолчанию
PORT = int(os.getenv("PORT", 8000))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

def clean_text(text: str):
    return text.strip().rstrip('?!.,').lower()

@dp.message(F.text)
async def check_message(message: Message):
    if not message.text:
        return
    if clean_text(message.text).endswith('да'):
        try:
            await message.reply("пизда")
        except Exception as e:
            print(f"Ошибка: {e}")

# --- ФУНКЦИИ ДЛЯ ВЕБ-СЕРВЕРА ---
async def handle(request):
    return web.Response(text="Бот работает!")

async def start_web_server():
    app = web.Application()
    app.add_routes([web.get('/', handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    # Важно: слушаем 0.0.0.0 и нужный порт
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()

# --- ГЛАВНАЯ ФУНКЦИЯ ---
async def main():
    # Запускаем веб-сервер и бота одновременно
    await start_web_server()
    print(f"Веб-сервер запущен на порту {PORT}")
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    if not TOKEN:
        sys.exit("Error: BOT_TOKEN not found.")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
