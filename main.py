from aiogram import Bot
import asyncio
import logging

from core.handlers.register_handlers import reg_router
from core.handlers.basic import dp
from core.settings import settings


async def start(dp):
    dp.include_router(reg_router)

    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start(dp))

