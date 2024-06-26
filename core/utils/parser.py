from datetime import datetime, timedelta, time
from typing import Tuple, Any


def date_parser(date):
    # 15,09,23
    #'2023-09-15'
    date_pars = date.split('.')
    day = int(date_pars[0])
    month = int(date_pars[1])
    year = int('20' + date_pars[2])

    date_lesson = datetime(year, month, day)

    return date_lesson


def main_date_parser(data):
    """ Получает словарь с данными урока от пользователя
    и создает объекты timedate для формированиея SQL запроса
    для записи урока в базу данных """

    # Получить данные из словаря
    date = data.get('date')
    start_lesson = data.get('start_time').split('.')
    duration_lesson = int(data.get('and_time'))

    # Получить дату урока в виде объекта datetime вида 2023-05-10 00:00:00
    date_lesson = datetime.strptime(date, "%d.%m.%y")

    # Получить время начала урока
    start_lesson = datetime(int(date_lesson.year), int(date_lesson.month),
                            int(date_lesson.day), int(start_lesson[0]),
                            int(start_lesson[1]))

    # Получить время окончания урока
    duration_lesson = timedelta(minutes=duration_lesson)
    end_lesson = start_lesson + duration_lesson

    date_dict = {
        'date': date_lesson,
        'start_lesson': start_lesson,
        'end_lesson': end_lesson
    }
    return date_dict

### Блок парсинга даты для красивого вывода пользователю ###
def get_two_digits(str_digit):
    str_digit = str(str_digit)
    if len(str_digit) == 1:
        str_digit = '0' + str_digit

    return str_digit

def pars_date(date):
    # Возвращает дату
    day = get_two_digits(date.day)
    month = get_two_digits(date.month)
    date = f'{day}.{month}'

    return date

def pars_time(date):
    # Возвращает время
    hour = get_two_digits(date.hour)
    minute = get_two_digits(date.minute)
    time = f'{hour}.{minute}'

    return time

##############################################################################


### Блок вывода расписания пользователю ###
def get_dict_lesson(cursor):
    # Принимает объект курсора со всеми столбцами из таблицы schedule
    # Получить данные по уроку из курсора, в курсоре может быть как один, таки больше одного урока,
    # возвращает список со словарем данных об уроке, либо словари с данными об уроках, если их несколько.
    list_dicts_lesson = []

    for lesson in cursor:
        id_lesson = lesson[0]
        date = lesson[1]
        start_lesson = lesson[2]
        end_lesson = lesson[3]


        dict_lessons = {
            'id_lesson': id_lesson,
            'date': date,
            'start_lesson': start_lesson,
            'end_lesson': end_lesson
        }

        list_dicts_lesson.append(dict_lessons)

    return list_dicts_lesson


def get_student_id_from_cursor(cursor, lesson_id=None):
    # Принимает объект курсора со столбцами student, visit, payment, comment из таблицы lessons_history
    # Возвращает словарь этих столбцов
    list_student_id_from_lesson = []

    # student, visit, payment, comment

    for lesson in cursor:
        student_id = lesson[0]
        party = lesson[1]
        visit = lesson[2]
        payment = lesson[3]
        comment = lesson[4]

        dict_student_id = {
            'student_id': student_id,
            'party_id': party,
            'visit': visit,
            'payment': payment,
            'comment': comment,
            'lesson_id': lesson_id
        }

        list_student_id_from_lesson.append(dict_student_id)

    return list_student_id_from_lesson


def get_student_id_from_party_cursor(cursor):
   # Получить id студентов из групп
    list_student_id_from_party = []

    # student, visit, payment, comment

    for party in cursor:
        student_id = party[0]
        list_student_id_from_party.append(student_id)

    tuple_id = tuple(list_student_id_from_party)

    return tuple_id


def get_party_from_cursor(cursor):
    list_party = []

    for party in cursor:
        party_id = party[0]
        create_date = party[1]
        update_date = party[2]
        name = party[3]
        active = party[4]

        dict_student_id = {
            'party_id': party_id,
            'create_date': create_date,
            'update_date': update_date,
            'name': name,
            'active': active
        }

        list_party.append(dict_student_id)

    return list_party


def get_list_student(cursor):
    list_students = []

    for student in cursor:
        student_id = student[0]
        first_name = student[1]
        middle_name = student[2]
        last_name = student[3]
        chat_id = student[16]


        dict_student_id = {
            'student_id': student_id,
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'chat_id': chat_id
        }

        list_students.append(dict_student_id)

    return list_students


def get_user_id(users: list) -> tuple[Any, ...]:
    list_user_id = []

    for user in users:
        user_id = user['student_id']
        list_user_id.append(user_id)

    tuple_id = tuple(list_user_id)

    return tuple_id


def get_party_id(parties: dict) -> tuple[Any, ...]:
    list_party_id = []

    for party in parties:
        party_id = party['party_id']
        list_party_id.append(party_id)

    tuple_id = tuple(list_party_id)

    return tuple_id


def get_lessons_id(lessons: dict) -> tuple[Any, ...]:
    list_lessons_id = []

    for lesson in lessons:
        lesson_id = lesson['id_lesson']
        list_lessons_id.append(lesson_id)

    tuple_id = tuple(list_lessons_id)

    return tuple_id

# (12, datetime.date(2023, 9, 16), datetime.time(18, 0), datetime.time(18, 45), None, None)
# (13, datetime.date(2023, 9, 16), datetime.time(21, 0), datetime.time(21, 45), None, None)









