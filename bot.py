import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import TOKEN
from app.handlers import router
from db.db import initialize_database

bot = Bot(TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    initialize_database()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Shutting down...')
