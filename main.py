import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command  # ВАЖНО: Нужен для работы /start
from aiohttp import web

# Получаем токен и порт из переменных окружения
TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 8000))

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция очистки текста (убирает знаки препинания и приводит к нижнему регистру)
def clean_text(text: str):
    return text.strip().rstrip('?!.,').lower()

# --- ХЕНДЛЕР 1: Команда /start (Должен быть ПЕРВЫМ) ---
@dp.message(Command("start"))
async def cmd_start(message: Message):
    try:
        await message.answer('Пожалуйста, введите слово "да" для начала работы с ботом')
    except Exception as e:
        print(f"Ошибка при ответе на start: {e}")

# --- ХЕНДЛЕР 2: Обработка текста (Срабатывает, если это не команда) ---
@dp.message(F.text)
async def check_message(message: Message):
    if not message.text:
        return
    
    # Логика проверки на "да"
    if clean_text(message.text).endswith('да'):
        try:
            await message.reply("пизда")
        except Exception as e:
            print(f"Ошибка отправки сообщения: {e}")

# --- НАСТРОЙКА ВЕБ-СЕРВЕРА (Для Koyeb) ---
async def handle(request):
    return web.Response(text="Бот работает стабильно!")

async def start_web_server():
    app = web.Application()
    app.add_routes([web.get('/', handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    # Слушаем порт 8000 (или тот, который дал Koyeb)
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()

# --- ЗАПУСК ---
async def main():
    # 1. Запускаем фейковый веб-сайт
    await start_web_server()
    print(f"Веб-сервер запущен на порту {PORT}")
    
    # 2. Удаляем вебхук (лечим ошибку TelegramConflictError)
    await bot.delete_webhook(drop_pending_updates=True)
    
    # 3. Запускаем самого бота
    print("Бот запущен и готов отвечать!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    if not TOKEN:
        sys.exit("Ошибка: Переменная окружения BOT_TOKEN не найдена.")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")
