from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command

from core.utils.statesform import StepForm
from requests_sql import add_user

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
    await message.answer('Введите отчество')
    await state.update_data(name=message.text)
    await state.set_state(StepForm.GET_MID_NAME)


@reg_router.message(StepForm.GET_MID_NAME)
async def get_name(message: Message, state: FSMContext):
    await message.answer('Введите фамилию')
    await state.update_data(mid_name=message.text)
    await state.set_state(StepForm.GET_LAST_NAME)


@reg_router.message(StepForm.GET_LAST_NAME)
async def get_last_name(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)

    context_data = await state.get_data()

    name = context_data.get('name')
    mid_name = context_data.get('mid_name')
    last_name = context_data.get('last_name')
    full_name_tg = message.from_user.full_name

    add_user(name, mid_name, last_name, message.from_user.id,
             full_name_telegram=full_name_tg)

    await message.answer(f'Вы успешно зарегистрировались, как '
                         f'{name} {mid_name} {last_name}')

    await state.clear()

