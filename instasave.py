import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from handlers import start, download

# Logging sozlamalari
logging.basicConfig(level=logging.INFO)

async def main():
    # Bot va dispatcher yaratish
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    
    # Routerlarni ulash
    dp.include_routers(
        start.router,
        download.router
    )
    
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
