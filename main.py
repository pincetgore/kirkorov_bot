import os
from fastapi import FastAPI, Request
from bot import telegram_app, TOKEN
import uvicorn

PORT = int(os.environ.get("PORT", 8000))
BASE_URL = os.environ.get("BASE_URL", "https://delicious-jaquelyn-pincetgorehome-cd382d55.koyeb.app")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{BASE_URL}{WEBHOOK_PATH}"

app = FastAPI()

@app.get("/")
async def healthcheck():
    return {"status": "ok"}

@app.post(WEBHOOK_PATH)
async def webhook(request: Request):
    data = await request.json()
    update = telegram_app.bot.de_json(data)
    await telegram_app.process_update(update)
    return {"ok": True}

if __name__ == "__main__":
    import asyncio
    # Устанавливаем webhook один раз
    asyncio.run(telegram_app.bot.set_webhook(WEBHOOK_URL))
    print(f"Webhook установлен: {WEBHOOK_URL}")
    # Запускаем uvicorn для FastAPI
    uvicorn.run("main:app", host="0.0.0.0", port=PORT)
