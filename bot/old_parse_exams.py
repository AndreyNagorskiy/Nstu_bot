import requests
from bs4 import BeautifulSoup as bs
import re



def get_courses_exams():
    # all_course_page_url = ['https://www.nstu.ru/entrance/entrance_all/bachelor?faculty=33', 'https://www.nstu.ru/entrance/entrance_all/bachelor?faculty=31',
    # 'https://www.nstu.ru/entrance/entrance_all/bachelor?faculty=38', 'https://www.nstu.ru/entrance/entrance_all/bachelor?faculty=39',
    # 'https://www.nstu.ru/entrance/entrance_all/bachelor?faculty=35', 'https://www.nstu.ru/entrance/entrance_all/bachelor?faculty=29',
    # 'https://www.nstu.ru/entrance/entrance_all/bachelor?faculty=40', 'https://www.nstu.ru/entrance/entrance_all/bachelor?faculty=32',
    # 'https://www.nstu.ru/entrance/entrance_all/bachelor?faculty=36', 'https://www.nstu.ru/entrance/entrance_all/bachelor?faculty=34']
    all_course_page_url = ['https://www.nstu.ru/entrance/entrance_all/bachelor?faculty=33']
    full_course_info = []
    session = requests.session()
    for href in all_course_page_url:
        request = session.get(href)
        if request.status_code == 200:
            soup = bs(request.content, 'lxml')
            faculty = soup.find('a', class_ = 'link-underlined link-black').text
            all_tr = soup.find_all('tr')
            for tr in all_tr:
                all_courses_name = str(tr.find('p')).split('<br')[0].replace('<p>', '')
                all_exams = tr.find_all('li')
                for exam in all_exams:
                    course_exams = re.sub(r'\d+', r'',exam.text).strip()      
                p_in_td= str(tr.select('td p'))
                try:
                    price = p_in_td.split('курс:')[1][:-9]
                    budget = p_in_td.split('Бюджетных:')[1].split('<')[0].strip()
                except:
                    pass
                


            

                # print(exams)

                # Находит весь текст, попробовать достать по-другому
                # ps = tr.find_all('p')
                # for p in ps:
                #     print(p.get_text())

                # a = test.split('курс:')[1][:-9]
                # b = test.split('курс:')[2][:-9]
                # c = test.split('курс:')[3][:-9]
                # print(f'1 - {a}')

            
 

get_courses_exams()




""" ПОПЫТКА СБОРА ЭКЗАМЕНОВ ДЕБИЛЬНЫМ ПУТЕМ"""

# test = exam.find_all('li')
# b = str(test)
# g = b.split('</li>')[0].replace('[<li><span class="hidden">1</span>', '')
# abc = exam.find('u').text
# gg = b.split('</li>')[2]




            # course_divs = soup.find_all('div', class_='spec-name-block')
            # info_divs = soup.find_all('div', class_='spec-details-block')
            # all_course_name = []
            # count_course = 0
            # for div in course_divs:
            #     course_name = div.find('a', class_='formitem_spec_name').text.replace('Направление ', '')
            #     all_course_name.append(course_name)


                # if course_name != 'None':
                #     all_course_name.append(course_name)