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








# with sqlite3.connect('nstu_bot_db.db') as db:
#     cursor = db.cursor()
#     query = """CREATE TABLE faculties(faculty TEXT PRIMARY KEY, information TEXT, decanat_cabinet TEXT,
#             decanat_phone TEXT, site_url TEXT) """
#     cursor.execute(query)