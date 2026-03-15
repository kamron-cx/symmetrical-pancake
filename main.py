import logging
import instaloader
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# --- SOZLAMALAR ---
API_TOKEN = '8633260476:AAFlCH9VjAX5ftfd4emmxR89as661R_EccE' # BotFather'dan olgan tokenni qo'ying
# GitHub'ga yuklangan sessiya faylingiz nomi
SESSION_FILE = 'telesaveinstabot' 

# Logging sozlamalari
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Instaloader ob'ektini sozlash
L = instaloader.Instaloader()

# --- SESSİYANI YUKLASH ---
try:
    # Sessiya faylini yuklaymiz
    L.load_session_from_file('telesaveinstabot', filename=SESSION_FILE)
    logging.info("Sessiya muvaffaqiyatli yuklandi.")
except FileNotFoundError:
    logging.error(f"Xatolik: '{SESSION_FILE}' fayli topilmadi! GitHub'ga yuklaganingizni tekshiring.")
except Exception as e:
    logging.error(f"Sessiya yuklashda kutilmagan xatolik: {e}")

# --- FUNKSIYALAR ---
def get_video_url(url):
    try:
        # Havoladan shortcode'ni ajratib olish
        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        if post.is_video:
            return post.video_url
        return None
    except Exception as e:
        logging.error(f"Instagramdan yuklashda xatolik: {e}")
        return None

# --- HANDLERLAR ---
@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    user_name = message.from_user.first_name
    await message.answer(f"Assalomu alaykum, {user_name}!\nInstagram video havolasini yuboring, men uni yuklab beraman.")

@dp.message_handler()
async def download_handler(message: types.Message):
    # Faqat instagram havolalarini tekshiramiz
    if "instagram.com" in message.text:
        wait_msg = await message.answer("Video tayyorlanmoqda, iltimos kuting... ⏳")
        
        try:
            video_url = get_video_url(message.text)

            if video_url:
                # Videoni yuborish
                await message.answer_video(video_url, caption="Bot tomonidan yuklab berildi ✅")
                await wait_msg.delete()
            else:
                await wait_msg.edit("Kechirasiz, video topilmadi yoki bu profil yopiq (sessiya xatosi).")
        except Exception as e:
            await wait_msg.edit(f"Xatolik yuz berdi: {e}")
    else:
        await message.answer("Iltimos, faqat Instagram video (Reels) havolasini yuboring.")

# --- BOTNI ISHGA TUSHIRISH ---
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

