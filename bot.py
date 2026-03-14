import os
import instaloader
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Bot tokeningizni kiriting
API_TOKEN = '8633260476:AAFlCH9VjAX5ftfd4emmxR89as661R_EccE'

# Logging sozlamalari
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
loader = instaloader.Instaloader()

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Salom! Menga Instagram post yoki video havolasini yuboring, men uni yuklab beraman.")

@dp.message_handler()
async def download_instagram(message: types.Message):
    link = message.text
    if "instagram.com" in link:
        temp_msg = await message.answer("Yuklanmoqda... 📥")
        try:
            # Havoladan qisqa kodni olish
            shortcode = link.split("/")[-2] if link.endswith("/") else link.split("/")[-1]
            if "?" in shortcode:
                shortcode = shortcode.split("?")[0]

            post = instaloader.Post.from_shortcode(loader.context, shortcode)

            if post.is_video:
                await message.answer_video(post.video_url, caption="Muvaffaqiyatli yuklandi! ✅")
            else:
                await message.answer_photo(post.url, caption="Muvaffaqiyatli yuklandi! ✅")
            
            await temp_msg.delete()
        except Exception as e:
            await message.answer(f"Xatolik yuz berdi: {e}")
            await temp_msg.delete()
    else:
        await message.answer("Iltimos, faqat Instagram havolasini yuboring.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)