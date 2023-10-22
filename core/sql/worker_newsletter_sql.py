import psycopg2
from core.sql.config_for_postgres import host, user, password, db_name
from core.sql import query_SQL
from core.utils.parser import get_list_student, get_dict_lesson, \
    get_student_id_from_cursor


def connect():
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True
    return connection


# Получить список уроков на указанную дату
def get_lessons_on_date(date):
    connection = False

    try:
        connection = connect()

        with connection.cursor() as cursor:
            query = query_SQL.get_lesson_on_date
            # Выполнение запроса
            cursor.execute(query, (date,))
            lessons = get_dict_lesson(cursor)
            print('[INFO] Data was succefully received')

            return lessons

    except Exception as ex:
        print('[INFO] Error while working with PostgreSQL', ex)

    finally:
        if connection:
            connection.close()
            print('[INFO] PostgreSQL connection closed')


def get_students_id_from_lesson_tomorrow(lessons_id):
    # получить id студентов которые записаны на урок и данные о посещении, оплате

    connection = False

    try:
        connection = connect()

        with connection.cursor() as cursor:
            query = query_SQL.get_student_id_from_history_tomorrow
            # Выполнение запроса
            cursor.execute(query, (lessons_id,))
            id_students = get_student_id_from_cursor(cursor, lessons_id)

            print('[INFO] Data was succefully received')

            return id_students

    except Exception as ex:
        print('[INFO] Error while working with PostgreSQL', ex)

    finally:
        if connection:
            connection.close()
            print('[INFO] PostgreSQL connection closed')
