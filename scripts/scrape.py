import requests
import json, csv
from urllib.parse import urljoin
from bs4 import BeautifulSoup

schools = {
    'FU': 'http://www.buchsys.de/fu-berlin/angebote/aktueller_zeitraum/{}',
    'HU': 'http://zeh2.zeh.hu-berlin.de/angebote/aktueller_zeitraum/{}',
    'HTW': 'http://sport.htw-berlin.de/angebote/aktueller_zeitraum/{}',
    'BEUTH': 'http://zeh02.beuth-hochschule.de/angebote/aktueller_zeitraum/{}',
    'UNI POTSDAM': 'http://buchung.hochschulsport-potsdam.de/angebote/aktueller_zeitraum/{}',
}

category_url = 'index_bereiche.html'
categories = dict()
for school_name, url in schools.items():
    soup = BeautifulSoup(requests.get(url.format(category_url)).text, 'html.parser')
    dl = soup.find_all('dl', attrs={'class': 'bs_menu'})[0]
    category = ''

    for element in dl.findChildren():
        if element.name == 'dt':
            category = element.text.replace(':', '')
        if element.name == 'a':
            href = url.format(element.attrs['href'])
            categories[href] = category

results = dict()
locations = dict()

temp = dict()
d = 0

f = open('courses.csv', 'wt')
try:
    writer = csv.writer(
        f,
        delimiter=';',
        lineterminator='\n',
        quoting=csv.QUOTE_NONNUMERIC)

    writer.writerow(['school_name', 'title', 'id', 'tage', 'zeit', 'ort', 'kursleiter', 'zeitraum', 'preise', 'status'])

    for school_name, url in schools.items():
        print(school_name, url)
        soup = BeautifulSoup(requests.get(url.format('index.html')).text, 'html.parser')

        for a in soup.find('dl', attrs={'class': 'bs_menu'}).find_all('a'):
            href = a.attrs['href']
            title = a.text
            print(title, href)
            if title == 'RESTPLÄTZE': continue
            s = BeautifulSoup(requests.get(url.format(href)).text, 'html.parser')

            for table in s.find_all('table', attrs={'class': 'bs_kurse'}):
                for row in table.find('tbody').find_all('tr'):
                    cols = row.find_all('td')

                    id         = cols[0].text
                    course_url = url.format(href)
                    details    = cols[1].text
                    tage       = cols[2].contents[0::2]
                    zeit       = cols[3].contents[0::2]
                    ort        = cols[4].text
                    zeitraum   = cols[5].text
                    kursleiter = cols[6].text

                    zeit = ['' if str(x) == '<br/>' else x for x in zeit]
                    tage = ['' if str(x) == '<br/>' else x for x in tage]

                    # TODO: add geolocations
                    # location_soup = BeautifulSoup(requests.get(urljoin(url, cols[4].find('a').attrs['href'])).text, 'lxml')
                    # qr = location_soup.find('img',{'id':'geo_qrcode'})
                    # geolocation = None
                    # if qr:
                    #     geolocation = qr.attrs['src'].split('q%')[1]
                    # print(ort, qr, geolocation)

                    try:
                        # TODO: fix shit
                        preise = str(cols[7].contents).replace('<br/>',' ').replace('</span>',' ').split('<div>')[0].split('>')[1]
                    except:
                        preise = cols[7].text
                    preise = preise.replace('\u00a0\u20ac','')
                    if len(preise.split('/ ')) > 0:
                        preise = preise.split('/ ' )

                    try:
                        status = cols[8].find('input').attrs['value']
                    except:
                        status = cols[8].text

                    if str(preise) not in temp:
                        temp[str(preise)] = 1
                    else:
                        temp[str(preise)] += 1

                    key = '{}_{}'.format(school_name, id)
                    results[key] = dict()
                    results[key]['school_name'] = school_name
                    results[key]['id'] = id
                    results[key]['title'] = title
                    results[key]['zeitraum'] = zeitraum
                    results[key]['preise'] = preise
                    results[key]['status'] = status
                    results[key]['ort'] = ort
                    results[key]['tage'] = []
                    results[key]['zeit'] = []
                    results[key]['url'] = course_url
                    results[key]['category'] = categories[course_url]

                    print(course_url)
                    try:
                        results[key]['description'] = str(s.find_all('div', attrs={'class': 'bs_kursbeschreibung'})[0].contents[0])
                    except:
                        pass

                    for i in range(len(tage)):
                        try:
                            results[key]['tage'].append(tage[i])
                            results[key]['zeit'].append(zeit[i])
                            writer.writerow([school_name, title, id, tage[i], zeit[i], ort, zeitraum, preise, status])
                        except:
                            try:
                                results[key]['tage'].append(tage[i])
                                results[key]['zeit'].append(zeit[0])
                                writer.writerow([school_name, title, id, tage[i], zeit[0], ort, zeitraum, preise, status])
                            except:
                                results[key]['tage'].append(tage[i])
                                writer.writerow([school_name, title, id, tage[i], None, ort, preise, status])
            d += 1

            try:
                tmp = results[key]
                print(json.dumps(tmp, ensure_ascii=False))
            except:
                print('banana')
            # if d > 15:
            #     break
finally:
    f.close()

json.dump(results, open('courses.json', 'w', encoding='utf-8'), sort_keys=True, indent=2, ensure_ascii=False)