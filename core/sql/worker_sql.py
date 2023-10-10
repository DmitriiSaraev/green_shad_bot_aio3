import psycopg2
from core.sql.config_for_postgres import host, user, password, db_name
from core.sql import query_SQL
from core.utils.parser import (get_dict_lesson, get_student_id_from_cursor,
                               get_party_from_cursor, get_list_student,
                               get_student_id_from_party_cursor)


def connect():
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True
    return connection


### Блок работы с пользователем ###
def create_table_users():
    connection = False

    try:
        connection = connect()
        with connection.cursor() as cursor:
            cursor.execute(query_SQL.create_table)
            print('[INFO] Table created successfully')
    except Exception as ex:
        print('[INFO] Error while working with PostgreSQL', ex)

    finally:
        if connection:
            connection.close()
            print('[INFO] PostgreSQL connection closed')


def add_user(first_name,
             middle_name,
             last_name,
             chat_id,
             birthday=None,
             gender=None,
             location=None,
             school=None,
             studies=False,
             role='student',
             status=None,
             id_kinsman=None,
             full_name_telegram=None,
             party=None,
             ):

    connection = False

    try:
        connection = connect()

        with connection.cursor() as cursor:
            query = query_SQL.create_user
            # Значения для вставки:
            values = (first_name, middle_name, last_name, birthday,
                      gender, location, school, studies, role, status,
                      id_kinsman,  full_name_telegram, party, chat_id)

            # Выполнение запроса
            cursor.execute(query, values)
            print('[INFO] Data was succefully inserted')

    except Exception as ex:
        print('[INFO] Error while working with PostgreSQL', ex)

    finally:
        if connection:
            connection.close()
            print('[INFO] PostgreSQL connection closed')


# Получить данные о пользователях по id
def get_user_data(list_id_user):
    connection = False

    try:
        connection = connect()

        with connection.cursor() as cursor:
            query = query_SQL.get_user_sql
            # Выполнение запроса
            cursor.execute(query, (list_id_user,))
            users = get_list_student(cursor)
            print('[INFO] Data was succefully received')

            return users

    except Exception as ex:
        print('[INFO] Error while working with PostgreSQL', ex)

    finally:
        if connection:
            connection.close()
            print('[INFO] PostgreSQL connection closed')


def get_party_data(parties_id):
    connection = False

    try:
        connection = connect()

        with connection.cursor() as cursor:
            query = query_SQL.get_party_sql
            # Выполнение запроса
            cursor.execute(query, (parties_id,))
            parties = get_party_from_cursor(cursor)
            print('[INFO] Data was succefully received')

            return parties

    except Exception as ex:
        print('[INFO] Error while working with PostgreSQL', ex)

    finally:
        if connection:
            connection.close()
            print('[INFO] PostgreSQL connection closed')


### Блок работы с расписанием ###

def add_lesson(date, start_lesson, end_lesson):
    connection = False

    try:
        connection = connect()

        with connection.cursor() as cursor:
            query = query_SQL.add_lesson
            # Значения для вставки:
            values = (date, start_lesson, end_lesson)
            # Выполнение запроса
            cursor.execute(query, values)
            print('[INFO] Data was succefully inserted')

    except Exception as ex:
        print('[INFO] Error while working with PostgreSQL', ex)

    finally:
        if connection:
            connection.close()
            print('[INFO] PostgreSQL connection closed')


# Получить все уроки которые еще будут, прошедшие не выдает
def get_all_future_lessons():
    connection = False

    try:
        connection = connect()

        with connection.cursor() as cursor:
            query = query_SQL.get_all_future_lessons
            # Выполнение запроса
            cursor.execute(query)
            dict_schedule = get_dict_lesson(cursor)
            print('[INFO] Data was succefully received')

            return dict_schedule

    except Exception as ex:
        print('[INFO] Error while working with PostgreSQL', ex)

    finally:
        if connection:
            connection.close()
            print('[INFO] PostgreSQL connection closed')


def get_lesson(lesson_id):
    # по id урока возвращает данные об уроке
    connection = False

    try:
        connection = connect()

        with connection.cursor() as cursor:
            query = query_SQL.get_lesson
            # Выполнение запроса
            cursor.execute(query, (lesson_id,))
            lesson = get_dict_lesson(cursor)

            print('[INFO] Data was succefully received')

            return lesson

    except Exception as ex:
        print('[INFO] Error while working with PostgreSQL', ex)

    finally:
        if connection:
            connection.close()
            print('[INFO] PostgreSQL connection closed')


def get_students_id_from_lesson(lesson_id):
    # получить id студентов которые записаны на урок и данные о посещении, оплате

    connection = False

    try:
        connection = connect()

        with connection.cursor() as cursor:
            query = query_SQL.get_student_id_from_history
            # Выполнение запроса
            cursor.execute(query, (lesson_id,))
            id_students = get_student_id_from_cursor(cursor)

            print('[INFO] Data was succefully received')

            return id_students

    except Exception as ex:
        print('[INFO] Error while working with PostgreSQL', ex)

    finally:
        if connection:
            connection.close()
            print('[INFO] PostgreSQL connection closed')


def get_active_party():
    # Получить все активные группы

    connection = False

    try:
        connection = connect()

        with connection.cursor() as cursor:
            query = query_SQL.get_active_party
            # Выполнение запроса
            cursor.execute(query)
            party = get_party_from_cursor(cursor)

            print('[INFO] Data was succefully received')

            return party

    except Exception as ex:
        print('[INFO] Error while working with PostgreSQL', ex)

    finally:
        if connection:
            connection.close()
            print('[INFO] PostgreSQL connection closed')


def add_party(date, name):
    # Создать группу

    connection = False

    try:
        connection = connect()

        with connection.cursor() as cursor:
            query = query_SQL.add_party
            # Значения для вставки:
            values = (date, name)
            # Выполнение запроса
            cursor.execute(query, values)
            print('[INFO] Data was succefully inserted')

    except Exception as ex:
        print('[INFO] Error while working with PostgreSQL', ex)

    finally:
        if connection:
            connection.close()
            print('[INFO] PostgreSQL connection closed')


# Получить список студентов без группы
def get_student_without_party():
    connection = False

    try:
        connection = connect()

        with connection.cursor() as cursor:
            query = query_SQL.get_student_without_party
            # Выполнение запроса
            cursor.execute(query)
            list_students = get_list_student(cursor)
            print('[INFO] Data was succefully received')

            return list_students

    except Exception as ex:
        print('[INFO] Error while working with PostgreSQL', ex)

    finally:
        if connection:
            connection.close()
            print('[INFO] PostgreSQL connection closed')


# Получить всех учеников
def get_all_students():
    connection = False

    try:
        connection = connect()

        with connection.cursor() as cursor:
            query = query_SQL.get_all_students
            # Выполнение запроса
            cursor.execute(query)
            list_students = get_list_student(cursor)
            print('[INFO] Data was succefully received')

            return list_students

    except Exception as ex:
        print('[INFO] Error while working with PostgreSQL', ex)

    finally:
        if connection:
            connection.close()
            print('[INFO] PostgreSQL connection closed')



def add_student_to_party_worker(create_date, party, student):
    # Добавить ученика в группу

    connection = False

    try:
        connection = connect()

        with connection.cursor() as cursor:
            query = query_SQL.add_student_in_party
            # Значения для вставки:
            values = (create_date, party, student)
            # Выполнение запроса
            cursor.execute(query, values)
            print('[INFO] Data was succefully inserted')

    except Exception as ex:
        print('[INFO] Error while working with PostgreSQL', ex)

    finally:
        if connection:
            connection.close()
            print('[INFO] PostgreSQL connection closed')


def add_party_id_to_users_worker(party_id, student_id):
    # Записать id группы в таблицу users

    connection = False

    try:
        connection = connect()

        with connection.cursor() as cursor:
            query = query_SQL.add_party_id_to_users
            # Значения для вставки:
            values = (party_id, student_id)
            # Выполнение запроса
            cursor.execute(query, values)
            print('[INFO] Data was succefully inserted')

    except Exception as ex:
        print('[INFO] Error while working with PostgreSQL', ex)

    finally:
        if connection:
            connection.close()
            print('[INFO] PostgreSQL connection closed')


def add_student_to_lesson_worker(lesson_id, student_id):
    # Записать ученика на урок

    connection = False

    try:
        connection = connect()

        with connection.cursor() as cursor:
            query = query_SQL.add_student_to_lesson
            # Значения для вставки:
            values = (lesson_id, None, student_id)
            # Выполнение запроса
            cursor.execute(query, values)
            print('[INFO] Ученик записан на урок')

    except Exception as ex:
        print('[INFO] Error while working with PostgreSQL', ex)

    finally:
        if connection:
            connection.close()
            print('[INFO] PostgreSQL connection closed')


def add_students_to_lesson_worker(lesson_id, student_ids, party_id):
    # Записать много учеников на урок

    connection = False

    try:
        connection = connect()

        with connection.cursor() as cursor:
            query = query_SQL.add_student_to_lesson

            # Создаем список кортежей для вставки
            values = [
                (lesson_id, party_id, student_id)
                for student_id in student_ids]

            # Выполнение запроса с множественными значениями
            cursor.executemany(query, values)

            print('[INFO] Ученик(и) записан(ы) на урок')

    except Exception as ex:
        print('[INFO] Error while working with PostgreSQL', ex)

    finally:
        if connection:
            connection.close()
            print('[INFO] PostgreSQL connection closed')



def add_party_to_lesson_worker(lesson_id, party_id):
    # Записать группу на урок

    connection = False

    try:
        connection = connect()

        with connection.cursor() as cursor:
            query = query_SQL.add_party_to_lesson
            # Значения для вставки:
            values = (lesson_id, party_id)
            # Выполнение запроса
            cursor.execute(query, values)
            print('[INFO] Группа записана на урок')

    except Exception as ex:
        print('[INFO] Error while working with PostgreSQL', ex)

    finally:
        if connection:
            connection.close()
            print('[INFO] PostgreSQL connection closed')



def delete_student_from_lesson(action, student_id, lesson_id):
    # Удалить студента с урока

    if action == 'delete_student_from_lesson':
        query = query_SQL.delete_student_from_lesson
    elif action == 'delete_party_from_lesson':
        query = query_SQL.delete_party_from_lesson

    connection = False

    try:
        connection = connect()

        with connection.cursor() as cursor:
            # Выполнение запроса
            cursor.execute(query, (student_id, lesson_id))
            id_students = get_student_id_from_cursor(cursor)

            print('[INFO] Data was succefully received')


    except Exception as ex:
        print('[INFO] Error while working with PostgreSQL', ex)

    finally:
        if connection:
            connection.close()
            print('[INFO] PostgreSQL connection closed')





def get_student_id_from_party(party_id):
    # получить id студентов из групп

    connection = False

    try:
        connection = connect()

        with connection.cursor() as cursor:
            query = query_SQL.get_student_id_from_party_sql
            # Выполнение запроса
            cursor.execute(query, (party_id,))
            id_students = get_student_id_from_party_cursor(cursor)

            print('[INFO] Data was succefully received')

            return id_students

    except Exception as ex:
        print('[INFO] Error while working with PostgreSQL', ex)

    finally:
        if connection:
            connection.close()
            print('[INFO] PostgreSQL connection closed')



# with connection.cursor() as cursor:
#     cursor.execute(
#         """SELECT nick_name FROM users WHERE first_name = 'Oleg';"""
#     )
#
#     # connection.commit()
#     print(cursor.fetchone())

# with connection.cursor() as cursor:
#     cursor.execute(
#         """DROP TABLE users;"""
#     )
#
#     print('[INFO] Table was deleted')

# except Exception as ex:
#     print('[INFO] Error while working with PostgreSQL', ex)
#
# finally:
#     if connection:
#         connection.close()
#         print('[INFO] PostgreSQL connection closed')

# try:
#     connection = psycopg2.connect(
#         host=host,
#         user=user,
#         password=password,
#         database=db_name
#     )
#     connection.autocommit = True

    # Версия сервера
    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         "SELECT version();"
    #     )
    #
    #     print(f'Server version: {cursor.fetchone()}')

    # Создать таблицу в базе данных
    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         """CREATE TABLE users(
    #             id serial PRIMARY KEY,
    #             first_name VARCHAR(50) NOT NULL,
    #             middle_name VARCHAR(50) NOT NULL,
    #             last_name VARCHAR(50) NOT NULL,
    #             birthday DATE,
    #             registration_date DATE DEFAULT CURRENT_DATE,
    #             full_name_telegram VARCHAR(255),
    #             chat_id INTEGER
    #             );"""
    #     )
    #
    #     # connection.commit()
    #     print('[INFO] Table created successfully')



