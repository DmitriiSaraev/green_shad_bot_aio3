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
        chat_id INTEGER
        );"""

create_user = """
                INSERT INTO users (
                first_name, middle_name, last_name,
                birthday, gender, location, school, studies, role, status,
                id_kinsman,  full_name_telegram, chat_id
                ) 
                VALUES (%s, %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s, %s, %s)
                """