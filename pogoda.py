from datetime import datetime
import requests
import pprint

def pars(city='Moscow'):
    API_KEY = 'cb5b309f7ca79a8a322e94d5f60c070d'
    URL = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'APPID': API_KEY, 
            'q' : city,
            'units': 'metric',
            'lang': 'ru' } 
    response = requests.get(URL, params=params) 
    result = response.json()
    return result

def pars_forecast(city='Moscow'):
    API_KEY = 'cb5b309f7ca79a8a322e94d5f60c070d'
    URL = 'http://api.openweathermap.org/data/2.5/forecast'
    params = {'APPID': API_KEY, 
            'q' : city,
            'units': 'metric',
            'lang': 'ru' }
    response = requests.get(URL, params=params)
    result = response.json()
    return result['list'][:5]

class Weather_today():
    """ Погода сегодня """
    def __init__(self, city='Moscow'):
        sl = pars(city)
        self.temp = sl['main']['temp']
        self.wind_speed = sl['wind']['speed']
        self.humidity = sl['main']['humidity']
        self.temp_max = sl['main']['temp_max']
        self.temp_min = sl["main"]['temp_min']
        self.weather = sl['weather'][0]['main']
        ts = sl['sys']['sunrise']
        dt = datetime.fromtimestamp(ts)
        self.sunrise = dt.strftime("%H:%M") 
        ts1 = sl['sys']['sunset']
        dt1 = datetime.fromtimestamp(ts1)
        self.sunset = dt1.strftime("%H:%M")
        
class Forecast():
    """ Прогноз погоды на ближайшие 15 часов """
    def __init__(self, city='Moscow'):
        li = pars_forecast(city)
        self.line5 = []
        for i in li:
            self.line5.append((i['dt_txt'], i['main']['temp'], i['weather'][0]['description']))
        
    def get_list(self):
        return self.line5

if __name__== '__main__':
    pprint("--------------------------------------------------------")
    pprint()
