from os import getenv
import asyncio
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
from handlers.routes import router

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
dp = Dispatcher()
dp.include_router(router)


async def main():
    bot = Bot(token=TOKEN)
    print("Starting bot...")

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopping bot...")
