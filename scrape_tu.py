import requests
import json, csv
from urllib.parse import urljoin
from bs4 import BeautifulSoup

base_url = 'https://www.tu-sport.de/index.php?id=2472'

soup = BeautifulSoup(requests.get(base_url).text, 'lxml')

for foo in soup.find_all('div', {'class': 'menu'}):
    for li in foo.find_all('li'):
        for a in li.find_all('a'):

            title = a.text
            href = a.attrs['href']

            if title == 'Aerobic':
                continue
            print(title, urljoin(base_url, href))

            s = BeautifulSoup(requests.get(urljoin(base_url, href)).text,'lxml')
            for row in s.find('table').find_all('tr'):
                for col in row.find_all('td'):
                    print(col.text.strip())

            # break
        # break
    break
