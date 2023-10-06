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
        status INT REFERENCES statuses (id),
        id_kinsman INTEGER,
        full_name_telegram VARCHAR(255),
        party INT REFERENCES party (id),
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
    end_lesson TIME,
    student INT REFERENCES users (id),
    party INT REFERENCES party (id)
);
"""


add_lesson = """
    INSERT INTO schedule(
    date, start_lesson, end_lesson  
    )
    VALUES (%s, %s, %s)
    """



craate_table_party = """CREATE TABLE IF NOT EXISTS party(
    id serial PRIMARY KEY,
    create_date DATE,
    update_date DATE,
    name VARCHAR(50),
    active BOOLEAN DEFAULT TRUE
);
"""

# Добавить группу
add_party = """
    INSERT INTO party(
    create_date, name
    )
    VALUES (%s, %s)
"""



# Создание таблицы Учеников в группе
craate_table_student_in_group = """CREATE TABLE IF NOT EXISTS student_in_group(
    id serial PRIMARY KEY,
    create_date DATE,
    update_date DATE,
    party INT REFERENCES party (id),
    student INT REFERENCES users (id),
    active BOOLEAN DEFAULT TRUE
);
"""


# Добавить ученика в группу
add_student_in_party = """
    INSERT INTO student_in_group(
    create_date, party, student  
    )
    VALUES (%s, %s, %s)
"""

# Добавить id группы в таблицу users
add_party_id_to_users = """
    UPDATE users
    SET party = %s
    WHERE id = %s;
"""


# Получить все активные группы
get_active_party = """
    SELECT * FROM party
    WHERE active = TRUE
"""



# Получить все уроки которые еще будут, прошедшие не выдает
get_all_future_lessons = """SELECT * FROM schedule
WHERE date > CURRENT_DATE OR 
(date = CURRENT_DATE AND start_lesson > CURRENT_TIME)
ORDER BY date, start_lesson
"""

# Получить урок по id
get_lesson = """
    SELECT *
    FROM schedule
    WHERE id = %s
"""

craate_table_lessons_history = """CREATE TABLE IF NOT EXISTS lessons_history(
    id serial PRIMARY KEY,
    id_lesson int,
    student INT REFERENCES users (id),
    party INT REFERENCES party (id),
    visit BOOl,
    payment BOOl,
    comment VARCHAR(255)
);
"""

delete_student_from_lesson = """
    DELETE FROM lessons_history WHERE id_lesson = %s AND student = %s
"""

# Получить список студентов и групп записанных на урок из таблицы история уроков
get_student_id_from_history = """
    SELECT student, party, visit, payment, comment FROM lessons_history
    WHERE id_lesson = %s
"""


# Получить юзеров по id
get_user_sql = """
SELECT * FROM users WHERE id IN %s
"""

# Получить группы по id
get_party_sql = """
SELECT * FROM party WHERE id IN %s
"""

# Получить список студентов без группы
get_student_without_party = """SELECT * FROM users
    WHERE party IS NULL"""

# Получить всех студентов
get_all_students = """SELECT * FROM users"""



add_student_to_lesson = """
    INSERT INTO lessons_history(
    id_lesson, student  
    )
    VALUES (%s, %s) 
"""


add_party_to_lesson = """
    INSERT INTO lessons_history(
    id_lesson, party  
    )
    VALUES (%s, %s) 
"""




craate_table_schedule = """CREATE TABLE IF NOT EXISTS statuses(
    id serial PRIMARY KEY,
    name VARCHAR(15) 
);
"""