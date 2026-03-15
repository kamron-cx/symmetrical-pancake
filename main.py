import logging
import instaloader
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Sozlamalar
API_TOKEN = '8633260476:AAFlCH9VjAX5ftfd4emmxR89as661R_EccE'
INSTA_USER = 'instauchuntgbot' # Sessiya fayli nomi shu bilan bog'liq bo'ladi

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Instaloader ob'ektini sozlash
L = instaloader.Instaloader()

# Saqlangan sessiyani yuklash
try:
    L.load_session_from_file(INSTA_USER)
    logging.info("Sessiya muvaffaqiyatli yuklandi.")
except FileNotFoundError:
    logging.error("Sessiya fayli topilmadi! Avval sessiyani saqlab oling.")

# Video yuklash funksiyasi
def get_video_url(url):
    try:
        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        
        if post.is_video:
            return post.video_url
        return None
    except Exception as e:
        logging.error(f"Xatolik: {e}")
        return None

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.answer("Sessiya orqali ishlovchi botga xush kelibsiz! Havola yuboring.")

@dp.message_handler()
async def download_handler(message: types.Message):
    if "instagram.com" in message.text:
        msg = await message.answer("Sessiya orqali yuklanmoqda...")
        video_url = get_video_url(message.text)
        
        if video_url:
            await message.answer_video(video_url)
            await msg.delete()
        else:
            await message.answer("Video topilmadi yoki xatolik yuz berdi.")
    else:
        await message.answer("Instagram havolasini yuboring.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
