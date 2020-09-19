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


def insert_course_info(name: str, values : tuple):
    sql = """ INSERT INTO {} ('course_name', 'faculty', 'level_education', 'price', 'budget')  VALUES (?,?,?,?,?)""".format(name)
    if conn is not None:
        try:
            conn.cursor().execute(sql,values)
            conn.commit()
        except Error as e:
            print(e)
    else:
        print("Error! cannot connect")

def insert_exams(values: tuple):
    sql = """ UPDATE courses 
    SET exams = ?
    WHERE course_name LIKE ?;"""
    if conn is not None:
        try:
            conn.cursor().execute(sql,values)
            conn.commit()
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


def get_courses_by_keys(keyNumber,keyValue):
    sql = """ SELECT course_name,faculty FROM courses
    WHERE {} = ?""".format(keyNumber)
    if conn is not None:
        try:
            info = conn.cursor().execute(sql, (keyValue,)).fetchall()
            return info
        except Error as e:
            print(e)
    else:
        print("Error! cannot connect")
