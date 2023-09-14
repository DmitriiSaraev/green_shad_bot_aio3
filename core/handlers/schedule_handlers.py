from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram import types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder


schedule_router = Router()

@schedule_router.message(Command('schedule'))
async def cmd_schedule(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text='Составить расписание',
        callback_data='make_a_schedule')
    )

    await message.answer(text='Нажми на кнопку - получишь результат!',
                         reply_markup=builder.as_markup())


@schedule_router.callback_query(F.data == 'make_a_schedule')
async def send_schedule(callback: types.CallbackQuery):
    await callback.message.answer(str('Лови расписание, йо мазафака'))

