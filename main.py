import asyncio
import logging

from aiogram import Bot, Dispatcher

from callbacks import callback_router
from database import create_table
from env import API_TOKEN
from handlers import handlers_router

logger = logging.getLogger(__name__)


async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()
    dp.include_routers(handlers_router, callback_router)
    logging.basicConfig(level=logging.INFO, filename="t_bot.log")
    await create_table()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
