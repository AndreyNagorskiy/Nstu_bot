import db

def get_faculties(message : str):
    raw = db.get_faculties(message)
    parsed = raw[1] + '\nКабинет деканата: ' + raw[2] + '\nТелефон: ' + raw[3] + '\nСайт: ' + raw[4]
    return parsed
