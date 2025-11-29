import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from aiohttp import web

# Получаем токен и порт
TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 8000))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция очистки текста (убирает знаки препинания и приводит к нижнему регистру)
def clean_text(text: str):
    return text.strip().rstrip('?!.,').lower()

# --- ХЕНДЛЕР 1: Команда /start ---
@dp.message(Command("start"))
async def cmd_start(message: Message):
    try:
        await message.answer('Пожалуйста, введите слово "да" для начала работы с ботом')
    except Exception as e:
        print(f"Ошибка start: {e}")

# --- ХЕНДЛЕР 2: Обработка текста (да / lf / йес) ---
@dp.message(F.text)
async def check_message(message: Message):
    if not message.text:
        return
    
    # Очищаем текст от мусора
    text = clean_text(message.text)
    
    # Условие 1: "да" или "lf" -> "пизда"
    if text.endswith('да') or text.endswith('lf'):
        try:
            await message.reply("пизда")
        except Exception as e:
            print(f"Ошибка отправки: {e}")
            
    # Условие 2: "йес" -> "хуйес"
    elif text.endswith('йес'):
        try:
            await message.reply("хуйес")
        except Exception as e:
            print(f"Ошибка отправки: {e}")

# --- ВЕБ-СЕРВЕР (Для Koyeb) ---
async def handle(request):
    return web.Response(text="Бот работает!")

async def start_web_server():
    app = web.Application()
    app.add_routes([web.get('/', handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()

# --- ЗАПУСК ---
async def main():
    await start_web_server()
    print(f"Веб-сервер запущен на порту {PORT}")
    
    # Удаляем вебхук для стабильности
    await bot.delete_webhook(drop_pending_updates=True)
    
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    if not TOKEN:
        sys.exit("Error: BOT_TOKEN not found.")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
