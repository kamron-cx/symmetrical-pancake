import os
import instaloader
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# --- SOZLAMALAR ---
# 1. Telegram Bot Tokeningizni bu yerga yozing (@BotFather dan olinadi)
API_TOKEN = 'SIZNING_BOT_TOKENINGIZ'

# 2. Instagram login ma'lumotlaringiz (Bot ishlashi uchun shart)
INSTA_USER = 'SIZNING_INSTAGRAM_LOGININGIZ'
INSTA_PASS = 'SIZNING_INSTAGRAM_PAROLINGIZ'

# Logging (Xatolarni kuzatish uchun)
logging.basicConfig(level=logging.INFO)

# Instaloader obyektini sozlash
loader = instaloader.Instaloader(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)

# Instagramga kirish
try:
    loader.login(INSTA_USER, INSTA_PASS)
    logging.info("Instagramga muvaffaqiyatli kirildi!")
except Exception as e:
    logging.error(f"Instagramga kirishda xatolik yuz berdi: {e}")

# Bot va Dispatcher obyektlari
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Assalomu alaykum! Menga Instagram post yoki video havolasini yuboring, men uni yuklab beraman.")

@dp.message_handler()
async def download_instagram(message: types.Message):
    link = message.text
    
    if "instagram.com" in link:
        temp_msg = await message.answer("Yuklanmoqda... 📥")
        try:
            # 1. Linkni tozalash (ortiqcha belgilarni olib tashlash)
            clean_link = link.split("?")[0].strip("/")
            
            # 2. Shortcode'ni ajratib olish
            shortcode = clean_link.split("/")[-1]

            # 3. Post ma'lumotlarini yuklash
            post = instaloader.Post.from_shortcode(loader.context, shortcode)

            # 4. Faylni yuborish (Video yoki Rasm)
            if post.is_video:
                await message.answer_video(post.video_url, caption="Muvaffaqiyatli yuklandi! ✅")
            else:
                await message.answer_photo(post.url, caption="Muvaffaqiyatli yuklandi! ✅")
            
            await temp_msg.delete()

        except Exception as e:
            logging.error(f"Xatolik: {e}")
            await message.answer(f"Xatolik yuz berdi: Instagram ma'lumot bera olmadi. Link noto'g'ri yoki profil yopiq bo'lishi mumkin.")
            await temp_msg.delete()
    else:
        await message.answer("Iltimos, faqat Instagram havolasini (link) yuboring.")

if __name__ == '__main__':
    # Botni ishga tushirish
    executor.start_polling(dp, skip_updates=True)
