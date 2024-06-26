from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.utils.parser import pars_date, pars_time
from core.utils.callback_data import (OpenLessonCallback, GetStudentForLesson,
                                      AddPartyToLesson, AddStudentToLesson,
                                      ShowPartyForAddToLesson,
                                      AddStudentToParty,
                                      ShowPartyForAddToStudent)


def get_inline_keyboard_for_admin():
    builder = InlineKeyboardBuilder()
    builder.button(text='Расписание',
                   callback_data='get_buttons_for_work_schedule')
    builder.button(text='Ученики',
                   callback_data='get_buttons_for_work_students')
    builder.button(text='Рассылка',
                   callback_data='newsletter')

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
        builder.button(text=f"{pars_date(lesson['date'])}, "
                            f"{pars_time(lesson['start_lesson'])} - "
                            f"{pars_time(lesson['end_lesson'])}",
                       callback_data=
                       OpenLessonCallback(id_lesson=lesson['id_lesson']))

    # Для вывовода по одной кномпке в ряду
    builder.adjust(*[1 for item in lessons])

    return builder.as_markup()


def get_keyboard_id_lesson(lesson):
    builder = InlineKeyboardBuilder()

    builder.button(text='Ученики',
                   callback_data=
                   GetStudentForLesson(id_lesson=int(lesson['id_lesson'])))
    builder.button(text='Изменить время',
                   callback_data=AddStudentToParty(
                       action='edit_date', lesson_id=int(lesson['id_lesson'])))
    builder.button(text='Отправить соообщение ученикам',
                   callback_data='send_message_lesson_student')
    builder.button(text='Отменить урок',
                   callback_data=AddStudentToParty(
                       action='delete_lesson',
                       lesson_id=int(lesson['id_lesson'])
                   ))

    builder.adjust(1, 1, 1, 1, 1, 1, 1)

    return builder.as_markup()

def get_keyboard_for_edit_lessons(lesson_id):
    builder = InlineKeyboardBuilder()

    builder.button(text='Изменить дату',
                   callback_data='edit_day')

    builder.button(text='Изменить время',
                   callback_data='edit_time')

    builder.button(text='Изменить длительность',
                   callback_data='edit_duration')

    builder.adjust(1, 1, 1)

    return builder.as_markup()


def get_inline_keyboard_add_student_to_lesson(lesson_id):
    # для записи ученика на урок
    builder = InlineKeyboardBuilder()
    builder.button(text='Записать группу',
                   callback_data=AddPartyToLesson(id_lesson=lesson_id))
    builder.button(text='Записать ученика',
                   callback_data=AddStudentToParty(
                       action='show_student_for_add_to_lesson',
                       lesson_id=lesson_id))

    return builder.as_markup()


def get_keyboard_recorded_student_to_lesson_and_edit_lesson(lesson_id,
                                                            students,
                                                            parties
                                                            ):
    # получить список учеников записанных на урок и кнопки для редактирования
    builder = InlineKeyboardBuilder()

    for student in students:
        builder.button(text=f'{student["first_name"]} {student["last_name"]}',
                       callback_data=AddStudentToParty(
                           action='open_student_card',  # Переделать
                           # при нажатии записывается на урок, а должна
                           # открываться карточка ученика
                           lesson_id=lesson_id),
                       student_id=student['student_id'])

    for party in parties:
        builder.button(text=f'{party["name"]}',
                       callback_data=AddStudentToParty(
                           action='open_party_card',
                           lesson_id=lesson_id,
                           party_id=party['party_id']))

    builder.button(text='Записать группу',
                   callback_data=AddPartyToLesson(id_lesson=lesson_id))
    builder.button(text='Записать ученика',
                   callback_data=AddStudentToParty(
                       action='show_student_for_add_to_lesson',
                       lesson_id=lesson_id))
    builder.button(text='Удалить ученика',
                   callback_data=AddStudentToParty(
                       action='show_student_for_delete_from_lesson',
                       lesson_id=lesson_id))

    builder.adjust(1, 1, *[1 for item in students])

    return builder.as_markup()


def keyboard_for_working_with_students():
    builder = InlineKeyboardBuilder()

    builder.button(text='Редактировать ученика',
                   callback_data='edit_student')
    builder.button(text='Добавить группу',
                   callback_data='add_party')
    builder.button(text='Добавить ученика в группу',
                   callback_data='add_student_to_party')

    builder.adjust(1, 1, 1)

    return builder.as_markup()


def keyboard_add_party_to_lesson(lesson_id, list_party):
    builder = InlineKeyboardBuilder()

    for party in list_party:
        builder.button(text=f'{party["name"]}',
                       callback_data=
                       ShowPartyForAddToLesson(lesson_id=lesson_id,
                                               party_id=party['party_id'],
                                               party_name=party['name']))

    builder.adjust(*[1 for item in list_party])
    return builder.as_markup()


def keyboard_get_students_without_group(action, students, lesson_id=None):
    # Вывести студентов для записи в группу
    builder = InlineKeyboardBuilder()

    for student in students:
        builder.button(text=f'{student["first_name"]} '
                            f'{student["middle_name"]} '
                            f'{student["last_name"]}',
                       callback_data=
                       AddStudentToParty(action=action,
                                         student_id=student["student_id"],
                                         lesson_id=lesson_id))

    builder.button(text='Показать всех учеников',
                   callback_data=AddStudentToParty
                   (action='show_all_students',
                    lesson_id=lesson_id))

    builder.adjust(1, *[1 for item in students])

    return builder.as_markup()


# Для выбора группы в котороую добавить ученика
def keyboard_add_student_to_party(student_id, list_party):
    builder = InlineKeyboardBuilder()

    for party in list_party:
        builder.button(text=f'{party["name"]}',
                       callback_data=
                       ShowPartyForAddToStudent(student_id=student_id,
                                                party_id=party['party_id']))

    builder.adjust(*[1 for item in list_party])
    return builder.as_markup()


def keyboard_choice_student_for_lesson(student_list, lesson_id):
    pass


def get_keyboard_delete_student_to_lesson(lesson_id, students, parties):
    # Получить список кого можно удалить
    builder = InlineKeyboardBuilder()
    if students:
        for student in students:
            builder.button(text=f'{student["first_name"]} {student["last_name"]}',
                           callback_data=AddStudentToParty(
                               action='delete_student_from_lesson',
                               lesson_id=lesson_id,
                               student_id=student['student_id']
                           ))

    if parties:
        for party in parties:
            builder.button(text=f'{party["name"]}',
                           callback_data=AddStudentToParty(
                               action='delete_party_from_lesson',
                               lesson_id=lesson_id,
                               party_id=party['party_id']))

    builder.adjust(*[1 for item in students])

    return builder.as_markup()
