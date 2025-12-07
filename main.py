import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiohttp import web

# Получаем токен и порт
TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 8000))

# Ссылка на донат
DONATE_LINK = "https://yoomoney.ru/to/ТВОЙ_КОШЕЛЕК"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- СПИСОК СЛОВ-ТРИГГЕРОВ ---
# да (рус), lf (раскладка), da (англ), дa (рус+англ), dа (англ+рус)
TARGET_WORDS = {'да', 'lf', 'da', 'дa', 'dа'}

# Функция очистки текста
def clean_text(text: str):
    # Убираем пробелы, знаки препинания справа (включая скобки, двоеточия)
    # И приводим всё к нижнему регистру
    return text.strip().rstrip('?!.,)(:;').lower()

# --- ХЕНДЛЕР 1: Команда /start ---
@dp.message(Command("start"))
async def cmd_start(message: Message):
    # Кнопка доната (отобразится только если ты заменил ссылку)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🍺 Поддержать автора", url=DONATE_LINK)]
    ]) if "ТВОЙ_КОШЕЛЕК" not in DONATE_LINK else None
    
    await message.answer(
        'Пожалуйста, введите слово "да" для начала работы с ботом',
        reply_markup=keyboard
    )

# --- ХЕНДЛЕР 2: Обработка текста ---
@dp.message(F.text)
async def check_message(message: Message):
    if not message.text:
        return
    
    # 1. Чистим текст
    cleaned_text = clean_text(message.text)
    
    # 2. Разбиваем на слова
    words = cleaned_text.split()
    
    if not words:
        return

    # 3. Берем последнее слово
    last_word = words[-1]
    
    # Условие 1: Проверяем, есть ли слово в нашем списке "TARGET_WORDS"
    # Это покроет и русское "да", и смешанное "дa", и "lf"
    if last_word in TARGET_WORDS:
        try:
            await message.reply("пизда")
        except Exception as e:
            print(f"Ошибка отправки: {e}")
            
    # Условие 2: "йес" -> "хуйес" (тут смешивание букв редко бывает, оставляем так)
    elif last_word == 'йес':
        try:
            await message.reply("хуйес")
        except Exception as e:
            print(f"Ошибка отправки: {e}")

# --- ВЕБ-СЕРВЕР ---
async def handle(request):
    return web.Response(text="Bot is running")

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
