from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_inline_keyboard_for_admin():
    builder = InlineKeyboardBuilder()
    builder.button(text='Расписание',
                   callback_data='get_buttons_for_work_schedule')
    builder.button(text='Ученики',
                   callback_data='get_buttons_for_work_students')

    # builder.adjust(1,1,1) сколько кнопок вывести в ряду
    # (по одной, в трех рядах)

    return builder.as_markup()


def get_inline_keyboard_for_schedule():
    builder = InlineKeyboardBuilder()
    builder.button(text='Просмотреть расписание',
                   callback_data='get_schedule')
    builder.button(text='Добавить урок',
                   callback_data='add_lesson')

    # builder.adjust(1,1,1) сколько кнопок вывести в ряду
    # (по одной, в трех рядах)

    return builder.as_markup()


