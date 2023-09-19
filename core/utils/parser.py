from datetime import datetime, timedelta, time


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
    and_lesson = start_lesson + duration_lesson

    date_dict = {
        'date': date_lesson,
        'start_lesson': start_lesson,
        'and_lesson': and_lesson
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
    list_dicts_lesson = []

    for lesson in cursor:
        id_lesson = lesson[0]
        date = lesson[1]
        start_lesson = lesson[2]
        and_lesson = lesson[3]
        student = lesson[4]
        party = lesson[5]

        dict_lessons = {
            'id_lesson': id_lesson,
            'date': date,
            'start_lesson': start_lesson,
            'and_lesson': and_lesson,
            'student': student,
            'party': party
        }

        list_dicts_lesson.append(dict_lessons)

    return list_dicts_lesson


# (12, datetime.date(2023, 9, 16), datetime.time(18, 0), datetime.time(18, 45), None, None)
# (13, datetime.date(2023, 9, 16), datetime.time(21, 0), datetime.time(21, 45), None, None)









