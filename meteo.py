import requests
from bs4 import BeautifulSoup as bs

class Meteo():
    def __init__(self):
        url = 'https://meteo.hr/podaci_e.php?section=podaci_vrijeme&prikaz=abc'
        self.soup = bs(requests.get(url).content,"html.parser")
        self.meteo_table = self.soup.find('tbody').find_all('tr')
        self.stations = {}
        for rows in self.meteo_table:
            self.station_data = rows.find_all('td')
            station_name = self.station_data[0].get_text().replace('\n','').strip()
            self.stations[station_name] = self.station_data[2].get_text()

#meteo_app = Meteo()
#print(meteo_app.temp())