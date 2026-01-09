from aiogram import Bot, Dispatcher, types
from config import TELEGRAM_TOKEN
from engine.resolver import resolve
from engine.fallback import manual
from render.compose import compose
from PIL import Image
import io

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
cache = {}

@dp.message()
async def handler(msg: types.Message):
    uid = msg.from_user.id
    if msg.photo:
        if uid not in cache:
            await msg.answer("Send title first.")
            return
        bg = Image.open(await msg.photo[-1].download())
        img = compose(bg, cache[uid])
        buf = io.BytesIO()
        img.save(buf,"PNG")
        buf.seek(0)
        await msg.answer_photo(types.BufferedInputFile(buf.read(),"thumb.png"))
        del cache[uid]
    else:
        data = resolve(msg.text)
        if not data:
            await msg.answer(manual())
        else:
            cache[uid]=data
            await msg.answer("Send background image.")
