import logging
import instaloader
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# --- SOZLAMALAR ---
API_TOKEN = '8633260476:AAFlCH9VjAX5ftfd4emmxR89as661R_EccE' 
SESSION_FILE = 'telesaveinstabot' 

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
L = instaloader.Instaloader()

# --- SESSİYANI YUKLASH ---
try:
    L.load_session_from_file('telesaveinstabot', filename=SESSION_FILE)
    logging.info("Sessiya muvaffaqiyatli yuklandi.")
except Exception as e:
    logging.error(f"Sessiya xatosi: {e}")

# --- ASOSIY FUNKSIYA ---
@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.answer("Assalomu alaykum! Menga Instagram havolasini yuboring, barcha rasm va videolarni yuklab beraman.")

@dp.message_handler()
async def download_handler(message: types.Message):
    if "instagram.com" in message.text:
        url = message.text.split('?')[0]
        wait_msg = await message.answer("Media fayllar tayyorlanmoqda... ⏳")
        
        try:
            shortcode = url.split("/")[-2]
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            
            media = types.MediaGroup()
            
            # 1. Agar bu karusel bo'lsa (bir nechta rasm/video)
            if post.typename == 'GraphSidecar':
                for node in post.get_sidecar_nodes():
                    if node.is_video:
                        media.attach_video(node.video_url)
                    else:
                        media.attach_photo(node.display_url)
            
            # 2. Agar bitta video bo'lsa
            elif post.is_video:
                media.attach_video(post.video_url)
            
            # 3. Agar bitta rasm bo'lsa
            else:
                media.attach_photo(post.display_url)

            # Media guruhni yuborish
            await message.answer_media_group(media)
            await wait_msg.delete()

        except Exception as e:
            logging.error(f"Xatolik: {e}")
            await wait_msg.edit("Xatolik yuz berdi. Havola to'g'riligini yoki profil ochiqligini tekshiring.")
    else:
        await message.answer("Iltimos, Instagram havolasini yuboring.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

