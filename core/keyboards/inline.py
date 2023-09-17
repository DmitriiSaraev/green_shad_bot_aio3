from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.utils.parser import pars_date, pars_time
from core.utils.callback_data import OpenLessonCallback


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


def get_keyboard_lessons(lessons):
    builder = InlineKeyboardBuilder()

    for lesson in lessons:
        builder.button(text=f"Дата: {pars_date(lesson['date'])}, \r\n"
                            f"Начало урока: "
                            f"{pars_time(lesson['start_lesson'])}\r\n"
                            f"Конец урока: {pars_time(lesson['and_lesson'])}",
                       callback_data=
                       OpenLessonCallback(id_lesson=lesson['id_lesson'],
                                          date=lesson['date'],
                                          start_lesson=lesson['start_lesson'],
                                          and_lesson=lesson['and_lesson'],
                                          student=lesson['student'],
                                          party=lesson['party']
                                          )
                       )

    builder.adjust(1, 1)

    # Для вывовода по одной кномпке в ряду
    # print(*[item + ', ' for item in pokemon_list])
    # Результат:
    # Pikachu,  Abra,  Charmander,

    return builder.as_markup()





