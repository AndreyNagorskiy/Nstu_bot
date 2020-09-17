import db

def get_faculties(message: str):
    raw = db.get_faculties(message)
    parsed = raw[1] + "\n" + raw[2] + '\nКабинет деканата: ' + raw[3] + '\nТелефон: ' + raw[4] + '\nСайт: ' + raw[5]
    return parsed


def get_faculties_contacts(message: str):
    raw = db.get_faculties(message)
    parsed = 'Кабинет деканата: ' + raw[3] + '\nТелефон: ' + raw[4] + '\nСайт: ' + raw[5] + '\nEmail: ' + raw[6]
    return parsed


def create_table_courses():
    name = 'courses'
    titles = '''course_name TEXT PRIMARY KEY,
    rating_link TEXT,
    faculty TEXT,
    budget TEXT,
    price TEXT,
    exams TEXT,
    pre_course TEXT,
    keys TEXT'''
    db.create_teble(name, titles)

def add_courses_info(info: list):
    for i in info:
        db.insert('courses', tuple(i.values()))
    
def get_courses_by_keys(key1,key2,key3):
    course_info = db.get_courses_by_keys((key1,key2,key3,))
    msg = 'Вам могут быть интересны направления:\n' 
    for course in course_info:
        msg += (course[0] + '\nФакультет - ' + course[1]+ '\n')
    return(msg)