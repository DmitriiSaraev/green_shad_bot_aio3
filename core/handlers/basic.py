from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from core.settings import settings
from core.utils.commands import set_commands
from core.utils.statesform import StepForm


dp = Dispatcher()


@dp.startup()
async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id,
                           text='Йоу, Димас, бот запущен!')


@dp.shutdown()
async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id,
                           text='Йоу, Димас, бот остановлен!')


@dp.message(CommandStart())
async def get_start(message: Message, bot: Bot):
    await message.answer(f'Привет {message.from_user.first_name},'
                         f' рад тебя видеть!')



