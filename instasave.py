import os
import re
import instaloader
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
import asyncio

# O'z tokeningni shu yerga yoz
BOT_TOKEN = "7154872123:AAHxxxxxxxxxxxxxxxxxxxxxxxxxx"  # @BotFather dan olingan token

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Salom! Instagram havolasini yubor, men yuklab beraman.")

@dp.message()
async def download(message: types.Message):
    url = message.text
    
    # Instagram havolasi ekanini tekshirish
    if "instagram.com" not in url:
        await message.answer("❌ Instagram havolasi yuboring!")
        return
    
    await message.answer("⏳ Yuklanmoqda...")
    
    try:
        # Shortcode ajratib olish
        shortcode = re.search(r'/p/([^/]+)', url)
        if not shortcode:
            shortcode = re.search(r'/reel/([^/]+)', url)
        
        if not shortcode:
            await message.answer("❌ Noto'g'ri havola!")
            return
        
        code = shortcode.group(1)
        
        # Instagram dan yuklab olish
        loader = instaloader.Instaloader()
        post = instaloader.Post.from_shortcode(loader.context, code)
        
        # Papka yaratish
        os.makedirs("downloads", exist_ok=True)
        
        if post.is_video:
            # Video yuklash
            file_path = f"downloads/{code}.mp4"
            loader.download_pic(url=post.video_url, filename=file_path, mtime=post.date_utc)
            
            # Bot ga yuborish
            await message.answer_video(FSInputFile(file_path))
        else:
            # Rasm yuklash
            file_path = f"downloads/{code}.jpg"
            loader.download_pic(url=post.url, filename=file_path, mtime=post.date_utc)
            
            # Bot ga yuborish
            await message.answer_photo(FSInputFile(file_path))
        
        # Faylni o'chirish
        os.remove(file_path)
        await message.answer("✅ Tayyor!")
        
    except Exception as e:
        await message.answer(f"❌ Xato: {str(e)}")

async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
