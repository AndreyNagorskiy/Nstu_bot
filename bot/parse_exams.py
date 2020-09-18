import requests
from bs4 import BeautifulSoup as bs
import re
import db_operations

def get_courses_exams():
    all_course_page_url = ['https://www.nstu.ru/entrance/entrance_all/bachelor?faculty=33', 'https://www.nstu.ru/entrance/entrance_all/bachelor?faculty=31',
    'https://www.nstu.ru/entrance/entrance_all/bachelor?faculty=38', 'https://www.nstu.ru/entrance/entrance_all/bachelor?faculty=39',
    'https://www.nstu.ru/entrance/entrance_all/bachelor?faculty=35', 'https://www.nstu.ru/entrance/entrance_all/bachelor?faculty=29',
    'https://www.nstu.ru/entrance/entrance_all/bachelor?faculty=40', 'https://www.nstu.ru/entrance/entrance_all/bachelor?faculty=32',
    'https://www.nstu.ru/entrance/entrance_all/bachelor?faculty=36', 'https://www.nstu.ru/entrance/entrance_all/bachelor?faculty=34']
    full_course_info = []
    session = requests.session()
    for href in all_course_page_url:
        request = session.get(href)
        if request.status_code == 200:
            soup = bs(request.content, 'lxml')
            faculty = soup.find('a', class_ = 'link-underlined link-black').text
            for tr in soup.find_all('tr'):
                exam_in_course = []
                all_courses_name = str(tr.find('p')).split('<br')[0].replace('<p>', '')
                for exam in tr.find_all('li'):
                    course_exams = re.sub(r'\d+', r'',exam.text).strip()
                    exam_in_course.append(course_exams)   
                data = {
                    'faculty':faculty,
                    'course_name':all_courses_name,
                    'exams': str(exam_in_course).strip('[]').replace("'", '')
                }
                if not any(i['course_name'] == data['course_name'] for i in full_course_info) and data['course_name'] != 'None':
                    full_course_info.append(data)
    return full_course_info


db_operations.add_exams(get_courses_exams())