import asyncio
import uvicorn
from bot import dp, bot
from server import app

async def start_bot():
    await dp.start_polling(bot)

def start_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

async def main():
    loop = asyncio.get_event_loop()
    loop.create_task(start_bot())
    start_server()

asyncio.run(main())
