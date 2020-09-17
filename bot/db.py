import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


conn = create_connection(r'./bot/database/nstu_bot_db.db')


def get_faculties(faculty: str):
    sql = """ SELECT * FROM faculties
	WHERE faculty = ? """
    if conn is not None:
        try:
            info = conn.cursor().execute(sql, (faculty,)).fetchall()
            return info[0]
        except Error as e:
            print(e)
    else:
        print("Error! cannot connect")


def insert(name: str, values : tuple):
    marks = ''
    for value in values: marks += '?,'
    sql = """
     INSERT INTO {} ('course_name', 'faculty', 'level_education', 'price', 'budget')  VALUES ({})""".format(name, marks[:-1])
    if conn is not None:
        try:
            conn.cursor().execute(sql,values)
        except Error as e:
            print(e)
    else:
        print("Error! cannot connect")


def create_teble(name: str, titles: str):
    sql = """ CREATE TABLE IF NOT EXISTS {0}
	({1})""".format(name, titles)
    if conn is not None:
        try:
            conn.cursor().execute(sql)
        except Error as e:
            print(e)
    else:
        print("Error! cannot connect")


