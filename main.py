import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from fastapi import FastAPI
import uvicorn
from generator import generate_thumbnail

BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 8000))

bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
app = FastAPI()

# store user states
user_sessions = {}


# -------- HEALTH CHECK ENDPOINT ----------
@app.get("/")
def root():
    return {"status": "alive"}


# -------- TELEGRAM HANDLERS ----------

@dp.message(F.text)
async def handle_title(message: types.Message):
    user_sessions[message.from_user.id] = {
        "title": message.text.strip(),
        "waiting_for_image": True
    }
    await message.reply("✅ Title saved. Now send the background image.")


@dp.message(F.photo)
async def handle_image(message: types.Message):
    uid = message.from_user.id

    if uid not in user_sessions:
        await message.reply("❌ Send the title first.")
        return

    title = user_sessions[uid]["title"]

    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file.file_path}"

    await message.reply("🧠 Generating poster...")

    try:
        out = await generate_thumbnail(title, file_url)
        await message.answer_photo(types.FSInputFile(out))
    except Exception as e:
        await message.reply(str(e))

    del user_sessions[uid]


# -------- RUN BOTH BOT + SERVER ----------
async def start():
    bot_task = asyncio.create_task(dp.start_polling(bot))
    server = uvicorn.Server(
        uvicorn.Config(app, host="0.0.0.0", port=PORT, log_level="info")
    )
    api_task = asyncio.create_task(server.serve())

    await asyncio.gather(bot_task, api_task)


if __name__ == "__main__":
    asyncio.run(start())
