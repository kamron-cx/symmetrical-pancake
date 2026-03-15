import logging
import instaloader
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# --- SOZLAMALAR ---
API_TOKEN = '8633260476:AAGO0oZEtL4iFeFenPmlqIpA4zdZiRkPqak' 
SESSION_FILE = 'telesaveinstabot' 

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
L = instaloader.Instaloader()

# --- SESSİYANI YUKLASH ---
try:
    L.load_session_from_file('telesaveinstabot', filename=SESSION_FILE)
    logging.info("Sessiya yuklandi.")
except Exception as e:
    logging.error(f"Sessiya xatosi: {e}")

# --- HANDLERLAR ---
@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.answer("Assalomu alaykum! Instagram havolasini yuboring.")

@dp.message_handler()
async def download_handler(message: types.Message):
    if "instagram.com" in message.text:
        url = message.text.split('?')[0]
        wait_msg = await message.answer("Media fayllar tayyorlanmoqda... ⏳")
        
        try:
            shortcode = url.split("/")[-2]
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            media = types.MediaGroup()
            
            # Karusel, Video yoki Rasmni tekshirish
            if post.typename == 'GraphSidecar':
                nodes = list(post.get_sidecar_nodes())[:10] # Maksimum 10 ta
                for node in nodes:
                    if node.is_video:
                        media.attach_video(node.video_url)
                    else:
                        media.attach_photo(node.display_url)
            elif post.is_video:
                media.attach_video(post.video_url)
            else:
                media.attach_photo(post.display_url)

            # Media guruhni yuborish
            await bot.send_media_group(chat_id=message.chat.id, media=media)
            await wait_msg.delete()

        except Exception as e:
            logging.error(f"Xatolik: {e}")
            await wait_msg.edit("Xatolik: Media yuklanmadi. Havola xato yoki profil yopiq bo'lishi mumkin.")
    else:
        await message.answer("Iltimos, Instagram havolasini yuboring.")

if __name__ == '__main__':
    # Ikkita nusxa bo'lib ishlamasligi uchun start_polling ishlatamiz
    executor.start_polling(dp, skip_updates=True)
