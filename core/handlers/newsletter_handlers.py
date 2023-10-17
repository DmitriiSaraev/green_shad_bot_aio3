from datetime import datetime, timedelta, time

from aiogram import F, Router, Bot
from aiogram import types

from core.keyboards.newsletter_inline_keyboard import (
    get_inline_keyboard_newsletter)
from core.sql.worker_newsletter_sql import get_lessons_on_date, \
    get_students_id_from_lesson_tomorrow
from core.sql.worker_sql import get_students_id_from_lesson, get_user_data
from core.utils.parser import get_lessons_id, get_user_id

newsletter_router = Router()


@newsletter_router.callback_query(F.data == 'newsletter')
async def get_buttons_for_working_with_students(callback: types.CallbackQuery):
    keyboard = get_inline_keyboard_newsletter()

    await callback.message.answer(text='Выбирай',
                                  reply_markup=keyboard)

    await callback.answer()


@newsletter_router.callback_query(F.data == 'send_reminder_tomorrow')
async def get_buttons_for_working_with_students(callback: types.CallbackQuery,
                                                bot: Bot):
    # Нужно получить всех пользователей у которых завтра уроки и отправить
    # напоминание

    today = datetime.now()

    tomorrow = (today + timedelta(days=1)).date()
    tomorrow_str = tomorrow.strftime('%Y-%m-%d')

    lessons = get_lessons_on_date(tomorrow_str)
    lessons_id = get_lessons_id(lessons)

    lessons_history = get_students_id_from_lesson_tomorrow(lessons_id)
    student_id = get_user_id(lessons_history)

    students = get_user_data(student_id)

    for student in students:
        await bot.send_message(student['chat_id'],
                               'Напоминаю что у вас завтра состоится урок')

    # await bot.send_message()




    # students = get_students_tomorrow()


    keyboard = get_inline_keyboard_newsletter()

    await callback.answer()