import requests
from bs4 import BeautifulSoup as bs
import db_operations
import pyshorteners


def get_links():
    courses = db_operations.get_course_names()
    for course in courses:
        request = requests.post('https://www.nstu.ru/entrance/admission_campaign/search_direction', data = {'keywords': course})
        soup = bs(request.content, 'lxml')
        link = pyshorteners.Shortener().clckru.short('https://www.nstu.ru/entrance/admission_campaign/' + soup.find(class_='formitem_spec_name').get('href'))
        rating_link = get_rating_links(course)
        db_operations.add_link((link,rating_link,course,))
        


def get_rating_links(course):
    request = requests.get('https://www.nstu.ru/entrance/admission_campaign/entrance')
    soup = bs(request.content, 'lxml')
    tables = soup.find_all('table')
    for table in tables:
        if course.replace(' -','') in table.find('b').text and 'очная' in table.text:
            return(table.find('a').get('href'))




get_links()
