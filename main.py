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

# Ссылка на донат (если используешь)
DONATE_LINK = "https://yoomoney.ru/to/ТВОЙ_КОШЕЛЕК" 

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция очистки текста
def clean_text(text: str):
    # Убираем пробелы по краям, затем знаки препинания справа
    # Добавил больше знаков: скобки, двоеточия и т.д.
    return text.strip().rstrip('?!.,)(:;').lower()

# --- ХЕНДЛЕР 1: Команда /start ---
@dp.message(Command("start"))
async def cmd_start(message: Message):
    # Создаем кнопку (опционально, если хочешь оставить донаты)
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
    
    # 1. Чистим текст от знаков препинания справа
    cleaned_text = clean_text(message.text)
    
    # 2. Разбиваем текст на отдельные слова по пробелам
    # Например: "Ну ты да..." -> очистится в "ну ты да" -> список ['ну', 'ты', 'да']
    words = cleaned_text.split()
    
    # Если слов нет (отправили только смайлики или знаки), выходим
    if not words:
        return

    # 3. Берем ПОСЛЕДНЕЕ слово из списка
    last_word = words[-1]
    
    # Условие 1: Последнее слово ИМЕННО "да" или "lf"
    # Теперь слова типа "вода", "беда" не пройдут проверку, так как "вода" != "да"
    if last_word == 'да' or last_word == 'lf':
        try:
            await message.reply("пизда")
        except Exception as e:
            print(f"Ошибка отправки: {e}")
            
    # Условие 2: Последнее слово ИМЕННО "йес"
    elif last_word == 'йес':
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
