from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command

from core.utils.statesform import StepForm

reg_router = Router()


@reg_router.message(F.text == 'Привет')
async def get_hello(message: Message, bot: Bot):
    await message.answer('И тебе привет!')


@reg_router.message(Command('register'))
async def get_register(message: Message, state: FSMContext):
    await message.answer(f'{message.from_user.first_name},'
                         f' начинаем регистрацию. Введите имя')
    await state.set_state(StepForm.GET_NAME)


@reg_router.message(StepForm.GET_NAME)
async def get_name(message: Message, state: FSMContext):
    await message.answer(f'Ваше имя:\r\n{message.text}\r\nТеперь '
                         f'введите фамилию')
    await state.update_data(name=message.text)
    await state.set_state(StepForm.GET_LAST_NAME)


@reg_router.message(StepForm.GET_LAST_NAME)
async def get_last_name(message: Message, state: FSMContext):
    await message.answer(f'Твоя фамилия:\r\n{message.text}\r\nтеперь '
                         f'введи возраст')
    await state.update_data(last_name=message.text)
    await state.set_state(StepForm.GET_AGE)


@reg_router.message(StepForm.GET_AGE)
async def get_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    context_data = await state.get_data()

    name = context_data.get('name')
    last_name = context_data.get('last_name')
    age = context_data.get('age')

    await message.answer(f'{name} {last_name}, '
                         f'твой возраст: {age}.')

    await state.clear()
