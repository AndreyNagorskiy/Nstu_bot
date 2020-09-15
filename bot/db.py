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

conn = create_connection(r'./database/nstu_bot_db.db')

def get_faculties(faculty : str):
	sql = """ SELECT * FROM faculties
	WHERE faculty = ? """
	if conn is not None:
		try:
			info = conn.cursor().execute(sql,(faculty,)).fetchall()
			return info[0]
		except Error as e:
			print(e)
	else:
		print("Error! cannot connect")

def create_teble(name: str, titles: str):
	sql = """ CREATE TABLE IF NOT EXISTS {0}
	({1})""".format(name,titles)
	if conn is not None:
		try:
			conn.cursor().execute(sql)
		except Error as e:
			print(e)
	else:
		print("Error! cannot connect")



# with sqlite3.connect('nstu_bot_db.db') as db:
#     cursor = db.cursor()
#     query = """CREATE TABLE faculties(faculty TEXT PRIMARY KEY, information TEXT, decanat_cabinet TEXT,
#             decanat_phone TEXT, site_url TEXT) """
#     cursor.execute(query)