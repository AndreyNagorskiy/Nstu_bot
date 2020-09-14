import requests
from bs4 import BeautifulSoup as bs
import csv




def get_course_href():
    all_course_href = []
    session = requests.session()
    faculty_url = 'https://www.nstu.ru/edu/chairs'
    request = session.get(faculty_url)
    if request.status_code == 200:
            soup = bs(request.content, 'lxml')
            divs = soup.select(".faculty-info__chairs > a")
            for div in divs:
                faculty_href = div.get('href') + '/study_activity/specs'
                all_course_href.append(faculty_href)
    # Удаление кафедр Института социальных технологий 
    del (all_course_href[-1], all_course_href[-2], all_course_href[-3], all_course_href[-4], all_course_href[-5])
    return all_course_href



def get_full_course_details():
    full_course_info = []
    session = requests.session()
    for href in get_course_href():
        request = session.get(href)
        if request.status_code == 200:
            soup = bs(request.content, 'lxml')
            course_divs = soup.find_all('div', class_ = 'spec-name-block')
            info_divs = soup.find_all('div', class_ = 'spec-details-block')
            all_course_name = []
            count_course = 0
            for div in course_divs:
                course_name = div.find('a', class_ = 'formitem_spec_name').text.replace('Направление ', '')
                all_course_name.append(course_name)
            for div in info_divs:
                text_html = str(div)
                faculty = div.find('a').text.split()[-1].replace('(', '').replace(')', '')
                level_education = text_html.split('<span class="bold">Уровень обучения: </span>')[1].split()[0]
                price = text_html.split('<span class="bold">Стоимость для обучающихся по контракту на первом курсе (в год) за 2020-2021 учебный год: </span>')[1].split()[0] + ' руб.'
                budget = text_html.split('<span class="bold">Наличие бюджетных мест: </span>')[1].split()[0]
                if budget != 'есть':
                    budget = 'нет'
                data ={
                        'course_name': all_course_name[count_course],
                        'faculty':faculty,
                        'level_education':level_education,
                        'price': price,
                        'budget':budget
                }
                full_course_info.append(data)
                count_course += 1
    return full_course_info





