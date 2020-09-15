import db


def get_faculties(message: str):
    raw = db.get_faculties(message)
    parsed = raw[1] + "\n" + raw[2] + '\nКабинет деканата: ' + \
        raw[3] + '\nТелефон: ' + raw[4] + '\nСайт: ' + raw[5]
    return parsed


def get_faculties_contacts(message: str):
    raw = db.get_faculties(message)
    parsed = 'Кабинет деканата: ' + \
        raw[3] + '\nТелефон: ' + raw[4] + \
        '\nСайт: ' + raw[5] + '\nEmail: ' + raw[6]
    return parsed


def create_table_courses():
    name = 'courses'
    titles ='''course_name TEXT PRIMARY KEY,
    rating_link TEXT,
    faculty TEXT,
    budget TEXT,
    price TEXT,
    exams TEXT,
    pre_course TEXT,
    keys TEXT'''
    db.create_teble(name,titles)

create_table_courses()