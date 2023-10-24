from core.sql.worker_sql import (
    create_table_users, create_table_schedule,
    create_table_party, create_table_student_in_group,
    create_table_lessons_history, create_table_statuses
)


def create_table():
    create_table_statuses()
    create_table_party()
    create_table_users()
    create_table_schedule()
    create_table_student_in_group()
    create_table_lessons_history()

