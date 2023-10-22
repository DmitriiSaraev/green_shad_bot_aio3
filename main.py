from aiogram import Bot
import asyncio
import logging

from core.handlers.newsletter_handlers import newsletter_router
from core.handlers.register_handlers import reg_router
from core.handlers.schedule_handlers import schedule_router
from core.handlers.basic import dp
from core.settings import settings
from core.utils.create_table import create_table


async def start(dp):
    dp.include_router(reg_router)
    dp.include_router(schedule_router)
    dp.include_router(newsletter_router)

    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')

    create_table()

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start(dp))

