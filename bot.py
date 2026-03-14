import os
import instaloader
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Bot tokeningizni bu yerga qo'ying
API_TOKEN = '8633260476:AAFlCH9VjAX5ftfd4emmxR89as661R_EccE'

# Logging sozlamalari (xatolarni terminalda ko'rish uchun)
logging.basicConfig(level=logging.INFO)

# Instagram brauzer ko'rinishida so'rov yuborishi uchun User-Agent sozlamasi
loader = instaloader.Instaloader(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Salom! Menga Instagram post yoki video havolasini yuboring, men uni yuklab beraman.")

@dp.message_handler()
async def download_instagram(message: types.Message):
    link = message.text
    
    if "instagram.com" in link:
        temp_msg = await message.answer("Yuklanmoqda... 📥")
        try:
            # 1. Linkni tozalash (?igsh=... qismini olib tashlash)
            clean_link = link.split("?")[0]
            
            # 2. Shortcode'ni ajratib olish
            # Link oxiri / bilan tugasa yoki tugamasa ham to'g'ri olish uchun:
            parts = clean_link.strip("/").split("/")
            shortcode = parts[-1]

            # 3. Post ma'lumotlarini yuklash
            post = instaloader.Post.from_shortcode(loader.context, shortcode)

            # 4. Video yoki Rasm ekanligini tekshirib yuborish
            if post.is_video:
                await message.answer_video(post.video_url, caption="Muvaffaqiyatli yuklandi! ✅")
            else:
                await message.answer_photo(post.url, caption="Muvaffaqiyatli yuklandi! ✅")
            
            await temp_msg.delete()

        except Exception as e:
            # Xatolikni batafsil ko'rish uchun
            logging.error(f"Xato: {e}")
            await message.answer(f"Xatolik yuz berdi: Instagram ma'lumot bera olmadi. Birozdan so'ng qayta urinib ko'ring.")
            await temp_msg.delete()
    else:
        await message.answer("Iltimos, faqat Instagram havolasini yuboring.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
