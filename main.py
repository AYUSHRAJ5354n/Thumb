import asyncio
import threading
import uvicorn
from bot import dp, bot
from server import app

def run_api():
    uvicorn.run(app, host="0.0.0.0", port=8000)

async def run_bot():
    await dp.start_polling(bot)

if __name__ == "__main__":
    threading.Thread(target=run_api, daemon=True).start()
    asyncio.run(run_bot())
