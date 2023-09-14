from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram import types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.keyboards.inline import get_inline_keyboard_for_schedule
from core.utils.statesform import StateSchedule
from core.utils.parser import date_parser
from core.sql.worker_sql import add_lesson


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
    await callback.answer()


@schedule_router.callback_query(F.data == 'get_buttons_for_work_schedule')
async def send_schedule(callback: types.CallbackQuery):
    await callback.message.answer(text='Что будешь делать?',
                         reply_markup=get_inline_keyboard_for_schedule())
    await callback.answer()


@schedule_router.callback_query(F.data == 'add_lesson')
async def send_schedule(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Введи дату урока в формате дд.мм.гг')
    await state.set_state(StateSchedule.INPUT_DATE)


@schedule_router.message(StateSchedule.INPUT_DATE)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(date=message.text)
    await message.answer('Введи время начала урока в формате чч.мм')
    await state.set_state(StateSchedule.INPUT_START_LESSON)


@schedule_router.message(StateSchedule.INPUT_START_LESSON)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(start_time=message.text)
    await message.answer('Введи время окончания урока в формате чч.мм')
    await state.set_state(StateSchedule.INPUT_AND_LESSON)


@schedule_router.message(StateSchedule.INPUT_AND_LESSON)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(and_time=message.text)

    context_data = await state.get_data()

    date = context_data.get('date')
    start_lesson = context_data.get('start_time')
    and_lesson = context_data.get('and_time')

    date = date_parser(date)

    lesson = add_lesson(date, start_lesson, and_lesson)

    await message.answer(f'Создан урок дата: {date}\r\n'
                         f'Время начала: {start_lesson}\r\n'
                         f'Конец урока: {and_lesson}')

    await state.clear()




