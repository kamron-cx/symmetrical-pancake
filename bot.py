import telebot
from telebot import types
import instaloader
import os
import shutil

# --- SOZLAMALAR ---
BOT_TOKEN = "8633260476:AAFlCH9VjAX5ftfd4emmxR89as661R_EccE"
INSTA_USER = "instauchuntgbot"
INSTA_PASS = "@Te140993lyt"

bot = telebot.TeleBot(BOT_TOKEN)
L = instaloader.Instaloader()

# Havolalarni vaqtincha saqlash uchun lug'at
url_storage = {}

# Instagramga kirish
try:
    L.login(INSTA_USER, INSTA_PASS)
    print("Instagram tizimiga ulanish muvaffaqiyatli!")
except Exception as e:
    print(f"Login xatosi: {e}")

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Salom! Menga Instagram Reels yoki Post linkini yuboring.")

@bot.message_handler(func=lambda message: "instagram.com" in message.text)
def handle_link(message):
    url = message.text
    user_id = message.from_user.id
    
    # Havolani vaqtincha saqlaymiz (Tugma xatosi bermasligi uchun)
    url_storage[user_id] = url
    
    markup = types.InlineKeyboardMarkup()
    btn_start = types.InlineKeyboardButton("🚀 Yuklashni boshlash", callback_data="start_dl")
    btn_cancel = types.InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel_dl")
    markup.add(btn_start, btn_cancel)
    
    bot.reply_to(message, "Media aniqlandi. Yuklashni tasdiqlaysizmi?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    
    if call.data == "start_dl":
        if user_id not in url_storage:
            bot.answer_callback_query(call.id, "Xatolik: Havola topilmadi.")
            return

        url = url_storage[user_id]
        bot.edit_message_text("Tayyorlanmoqda... 🔄", call.message.chat.id, call.message.message_id)
        
        try:
            # Linkdan shortcode ajratish
            shortcode = url.split("/")[-2] if url.endswith("/") else url.split("/")[-1]
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            
            download_path = f"dir_{shortcode}"
            L.download_post(post, target=download_path)
            
            # Fayllarni saralash va yuborish
            files = os.listdir(download_path)
            for file in files:
                f_path = os.path.join(download_path, file)
                if file.endswith(".mp4"):
                    with open(f_path, 'rb') as v:
                        bot.send_video(call.message.chat.id, v, caption="🎬 Reels yuklab olindi.")
                elif file.endswith(".jpg"):
                    with open(f_path, 'rb') as p:
                        bot.send_photo(call.message.chat.id, p, caption="📸 Post rasmi yuklab olindi.")
            
            # Tozalash
            shutil.rmtree(download_path)
            del url_storage[user_id]
            bot.delete_message(call.message.chat.id, call.message.message_id)

        except Exception as e:
            bot.send_message(call.message.chat.id, f"Xatolik yuz berdi: {e}")
            
    elif call.data == "cancel_dl":
        if user_id in url_storage:
            del url_storage[user_id]
        bot.edit_message_text("Amal bekor qilindi.", call.message.chat.id, call.message.message_id)

bot.infinity_polling()
