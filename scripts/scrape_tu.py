import requests
import json, csv
from urllib.parse import urljoin
from urllib.parse import parse_qs
from bs4 import BeautifulSoup

base_url = 'https://www.tu-sport.de/index.php?id=2472'

soup = BeautifulSoup(requests.get(base_url).text, 'lxml')

results = json.load(open('courses.json', 'r'))

f = open('courses_tu.csv', 'wt')
try:
    writer = csv.writer(
        f,
        delimiter=';',
        lineterminator='\n',
        quoting=csv.QUOTE_NONNUMERIC)

    for foo in soup.find_all('div', {'class': 'menu'}):
        for li in foo.find_all('li'):
            for a in li.find_all('a'):
                title = a.text
                href = a.attrs['href']
                print(title, urljoin(base_url, href))

                if title in ['Aerobic', 'Anleitung Langhanteltraining', 'Badminton Courtmiete Semester', 'Teilzeitanmeldung für Berlin-Gäste',]:
                    continue

                s = BeautifulSoup(requests.get(urljoin(base_url, href)).text,'lxml')
                for row in s.find('tbody').find_all('tr'):
                    cols = row.find_all('td')
                    if len(cols) not in [3,10]:
                        continue

                    school_name = 'TU'
                    id = parse_qs(href)['cHash'][0]
                    tage = None
                    zeit = None
                    ort = None
                    zeitraum = None
                    preise = None
                    status = None

                    print(id, title)

                    if len(cols) == 10:
                        zielgruppe = cols[1].find('span').text
                        zeitraum = cols[3].text
                        tag = cols[4].find('abbr').text
                        zeit = cols[5].text
                        ort = cols[6].text.strip()
                        kursleiter = cols[7].text.strip()
                        preise = cols[8].find('abbr').text
                        status = cols[9].text.strip()

                    if len(cols) == 3:
                        tag = cols[0].find('abbr').text
                        zeit = cols[1].text
                        ort = cols[2].text.strip()

                    key = '{}_{}'.format(school_name, id)
                    results[key] = dict()
                    results[key]['school_name'] = school_name
                    results[key]['id'] = id
                    results[key]['title'] = title
                    results[key]['zeitraum'] = zeitraum
                    results[key]['preise'] = preise
                    results[key]['status'] = status
                    results[key]['ort'] = ort
                    if 'tage' not in results[key]:
                        results[key]['tage'] = []
                    if 'zeit' not in results[key]:
                        results[key]['zeit'] = []

                    results[key]['tage'].append(tag)
                    results[key]['zeit'].append(zeit)



                    writer.writerow([school_name, title, id, tage, zeit, ort, zeitraum, preise, status])
finally:
    f.close()


json.dump(results, open('courses.json', 'w'), sort_keys=True, indent=2, ensure_ascii=False)
