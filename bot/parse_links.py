import requests
from bs4 import BeautifulSoup as bs
import db_operations
import pyshorteners


def get_links():
    courses = db_operations.get_course_names()
    for course in courses:
        request = requests.post('https://www.nstu.ru/entrance/admission_campaign/search_direction', data = {'keywords': course})
        soup = bs(request.content, 'lxml')
        link = pyshorteners.Shortener().tinyurl.short('https://www.nstu.ru/entrance/admission_campaign/' + soup.find(class_='formitem_spec_name').get('href'))
        db_operations.add_link((link,course,))

get_links()