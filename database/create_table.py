import sqlite3

with sqlite3.connect('nstu_bot_db.db') as db:
    cursor = db.cursor()
    query = """CREATE TABLE faculties(faculty TEXT PRIMARY KEY, information TEXT, decanat_cabinet TEXT,
            decanat_phone TEXT, site_url TEXT) """
    cursor.execute(query)