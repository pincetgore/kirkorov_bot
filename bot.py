import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

# Получаем токен из переменных окружения (безопасность)
TOKEN = os.getenv("8366843143:AAHYOuS-QdfpVX2KA6q9T0GW_-lx1fvioQw")

# Включаем логирование, чтобы видеть ошибки в консоли
logging.basicConfig(level=logging.INFO)

# Инициализируем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция очистки текста от знаков препинания в конце
def clean_text(text: str):
    # Убираем пробелы и знаки препинания справа, приводим к нижнему регистру
    return text.strip().rstrip('?!.,').lower()

# Хендлер: срабатывает на ЛЮБОЕ текстовое сообщение
@dp.message(F.text)
async def check_message(message: Message):
    if not message.text:
        return
    
    # Проверяем, заканчивается ли очищенный текст на "да"
    # Это сработает на "Да", "ДА", "ну да", "да?" и т.д.
    if clean_text(message.text).endswith('да'):
        # Отвечаем на сообщение (reply)
        try:
            await message.reply("пизда")
        except Exception as e:
            # Обработка случая, если у бота нет прав писать в чат
            print(f"Ошибка отправки: {e}")

# Запуск процесса (polling)
async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Проверка наличия токена
    if not TOKEN:
        sys.exit("Ошибка: Переменная окружения BOT_TOKEN не найдена.")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")
