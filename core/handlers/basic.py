from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from core.settings import settings
from core.utils.commands import set_commands
from core.settings import settings
from core.keyboards.inline import get_inline_keyboard_for_admin


dp = Dispatcher()


@dp.startup()
async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id,
                           text='Бот запущен!')


@dp.shutdown()
async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id,
                           text='Бот остановлен!')


@dp.message(CommandStart())
async def get_start(message: Message, bot: Bot):
    if (message.from_user.id == settings.bots.admin_id
            or message.from_user.id == settings.bots.alyona_id):
        await message.answer('Вот что ты можешь выбрать',
                             reply_markup=get_inline_keyboard_for_admin())
    else:
        await message.answer(f'Привет {message.from_user.first_name},'
                         f' рад тебя видеть!')













