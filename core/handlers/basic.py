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


# @dp.message(F.text == 'Привет')
# async def get_hello(message: Message, bot: Bot):
#     await message.answer('И тебе привет!')


# @dp.message(Command('register'))
# async def get_register(message: Message, state: FSMContext):
#     await message.answer(f'{message.from_user.first_name},'
#                          f' начинаем регистрацию. Введите имя')
#     await state.set_state(StepForm.GET_NAME)
#
#
# @dp.message(StepForm.GET_NAME)
# async def get_name(message: Message, state: FSMContext):
#     await message.answer(f'Ваше имя:\r\n{message.text}\r\nТеперь '
#                          f'введите фамилию')
#     await state.update_data(name=message.text)
#     await state.set_state(StepForm.GET_LAST_NAME)
#
#
# @dp.message(StepForm.GET_LAST_NAME)
# async def get_last_name(message: Message, state: FSMContext):
#     await message.answer(f'Твоя фамилия:\r\n{message.text}\r\n теперь '
#                          f'введи возраст')
#     await state.update_data(last_name=message.text)
#     await state.set_state(StepForm.GET_AGE)
#
#
# @dp.message(StepForm.GET_AGE)
# async def get_age(message: Message, state: FSMContext):
#     await message.answer(f'Твой возраст:\r\n{message.text}\r\n')
#     await state.update_data(age=message.text)
#     context_data = await state.get_data()
#
#     name = context_data.get('name')
#     last_name = context_data.get('last_name')
#     age = context_data.get('age')
#
#     await message.answer(f'{name} {last_name}, '
#                          f'твой возраст: {age}.')
#
#     await state.clear()








