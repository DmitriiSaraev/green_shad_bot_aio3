import psycopg2
from core.sql.config_for_postgres import host, user, password, db_name
from core.sql import query_SQL
from core.utils.parser import get_dict_lesson


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



### Блок работы с расписанием ###

def add_lesson(date, start_lesson, and_lesson):
    connection = False

    try:
        connection = connect()

        with connection.cursor() as cursor:
            query = query_SQL.add_lesson
            # Значения для вставки:
            values = (date, start_lesson, and_lesson)
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



