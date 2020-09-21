import requests
from bs4 import BeautifulSoup as bs

def parser(link:str,name):
    request = requests.get(link)
    soup = bs(request.content, 'lxml')
    rows = soup.find_all('tr')
    place = ''
    for row in rows:
         tds = row.find_all('td')
         try:
             if tds[2].text == name:
                 place = tds[0].text                 
         except:
             pass
    return place
