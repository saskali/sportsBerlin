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
                    details    = cols[1].text
                    tage        = cols[2].contents[0::2]
                    zeit       = cols[3].contents[0::2]
                    ort        = cols[4].text
                    zeitraum   = cols[5].text
                    kursleiter = cols[6].text


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

                    # print(id, tage, zeit, ort, zeitraum, preise, status)
                    for i in range(len(tage)):
                        try:
                            writer.writerow([school_name, title, id, tage[i], zeit[i], ort, zeitraum, preise, status])
                        except:
                            try:
                                writer.writerow([school_name, title, id, tage[i], zeit[0], ort, zeitraum, preise, status])
                            except:
                                writer.writerow([school_name, title, id, tage[i], None, ort, preise, status])
            d += 1
            # if d > 15:
            # break
finally:
    f.close()