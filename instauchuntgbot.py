import instaloader

L = instaloader.Instaloader()

# O'z ma'lumotlaringizni yozing
USER = 'instauchuntgbot'  # Instagram loginigiz
PASS = 'Te140993lyt' # Instagram parolingiz

try:
    # Tizimga kirish
    L.login(USER, PASS)
    # Sessiyani faylga saqlash
    L.save_session_to_file(filename='instauchuntgbot')
    print("Sessiya fayli muvaffaqiyatli yaratildi!")
except Exception as e:
    print(f"Xatolik: {e}")