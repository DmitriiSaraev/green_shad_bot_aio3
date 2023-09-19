create_table = """CREATE TABLE IF NOT EXISTS users(
        id serial PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        middle_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        birthday DATE,
        gender VARCHAR(7),
        location VARCHAR(30),
        school INTEGER,
        registration_date DATE DEFAULT CURRENT_DATE,
        update_date DATE DEFAULT CURRENT_DATE,
        studies BOOLEAN DEFAULT FALSE,
        role VARCHAR(10),
        status VARCHAR(7),
        id_kinsman INTEGER,
        full_name_telegram VARCHAR(255),
        party VARCHAR(255),
        chat_id INTEGER
        );"""

create_user = """
                INSERT INTO users (
                first_name, middle_name, last_name,
                birthday, gender, location, school, studies, role, status,
                id_kinsman,  full_name_telegram, party, chat_id
                ) 
                VALUES (%s, %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s, %s)
                """


craate_table_schedule = """CREATE TABLE IF NOT EXISTS schedule(
    id serial PRIMARY KEY,
    date DATE,
    start_lesson TIME,
    and_lesson TIME,
    student INT REFERENCES users (id),
    party INT REFERENCES party (id)
);
"""


add_lesson = """
    INSERT INTO schedule(
    date, start_lesson, and_lesson  
    )
    VALUES (%s, %s, %s)
    """



craate_table_party = """CREATE TABLE IF NOT EXISTS party(
    id serial PRIMARY KEY,
    create_date DATE,
    update_date DATE,
    name VARCHAR(50)
);
"""


# Получить все уроки которые еще будут, прошедшие не выдает
get_all_future_lessons = """SELECT * FROM schedule
WHERE date > CURRENT_DATE OR 
(date = CURRENT_DATE AND start_lesson > CURRENT_TIME)
ORDER BY date, start_lesson
"""


get_lesson = """
    SELECT *
    FROM schedule
    WHERE id = %s
"""

