import os
import struct
import ctypes
import pogoda   
from datetime import datetime
import sqlite3
import random
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QApplication
from PyQt5 import QtGui
import sys

DIR = os.path.abspath(os.curdir)
FOLDER = 'photo_img'


def mixwallpaper(path):
    """ Меняем фон рабочего стола """
    if struct.calcsize('P') * 8 == 64:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)
    else:
        ctypes.windll.user32.SystemParametersInfoA(20, 0, path, 3)


def change_theme():
    """ Функция возвращает тему """
    seg = datetime.now()
    mes = seg.month
    hrs = seg.hour
    theme_name = ''
    zima = [12, 1, 2]
    leto = [6, 7, 8]
    ov = [9, 10, 11, 3, 4, 5]
    if mes in zima:
        if hrs >= 17:
            if weather.weather == 'Clouds':
                theme_name = 'зима_ночь_переменная облачность'
            elif weather.weather == 'Clear':
                theme_name = 'зима_ночь_ясно'
            elif weather.weather == 'Snow':
                theme_name = 'зима_ночь_снег'
            elif float(weather.temp) <= 5.3:
                theme_name = 'зима_ночь_туман'
        else:
            if weather.weather == 'Clouds':
                theme_name = 'зима_день_переменная облачность'
            elif weather.weather == 'Clear':
                theme_name = 'зима_день_ясно'
            elif weather.weather == 'Snow':
                theme_name = 'зима_день_снег'
            elif float(weather.temp) <= 5.3:
                theme_name = 'зима_день_туман'
    if mes in leto:
        if hrs >= 17:
            if weather.weather == 'Clouds':
                if weather.humidity >= 50:
                    theme_name = 'лето_ночь_пасмурно'
                else:
                    theme_name = 'лето_ночь_переменная_облачность'
            elif weather.weather == 'Clear':
                theme_name = 'лето_ночь_ясно'
            elif float(weather.temp) <= 5.3:
                theme_name = 'лето_ночь_туман'
            elif weather.weather == 'Rain':
                theme_name = 'лето_ночь_дождь'
        else:
            if weather.weather == 'Clouds':
                if weather.humidity >= 50:
                    theme_name = 'лето_день_пасмурно'
                else:
                    theme_name = 'лето_день_переменная_облачность'
            elif weather.weather == 'Clear':
                theme_name = 'лето_день_ясно'
            elif float(weather.temp) <= 5.3:
                theme_name = 'лето_день_туман'
            elif weather.weather == 'Rain':
                theme_name = 'лето_день_дождь'
    if mes in ov:
        if hrs >= 19:
            if weather.weather == 'Clouds':
                if weather.humidity >= 50:
                    theme_name = 'во_ночь_пасмурно'
                else:
                    theme_name = 'во_ночь_переменная_облачность'
            elif weather.weather == 'Clear':
                theme_name = 'во_ночь_ясно'
            elif weather.weather == 'Snow':
                theme_name = 'во_ночь_снег'
            elif weather.weather == 'Rain':
                theme_name = 'во_ночь_дождь'
        else:
            if weather.weather == 'Clouds':
                if weather.humidity >= 50:
                    theme_name = 'во_день_пасмурно'
                else:
                    theme_name = 'во_день_переменная_облачность'
            elif weather.weather == 'Clear':
                theme_name = 'во_день_ясно'
            elif weather.weather == 'Snow':
                theme_name = 'во_день_снег'
            elif weather.weather == 'Rain':
                theme_name = 'во_ночь_дождь'
    db(theme_name)


def db(name):
    """ Берет из базы данных необходимый файл """
    con = sqlite3.connect("data.sqlite3")
    cur = con.cursor()
    result = cur.execute("""SELECT link FROM oboi
    WHERE theme = (SELECT id FROM themes WHERE title = ?) """, (name,)).fetchall()

    elem = random.choice(result)
    if elem:
        file_name = elem[0]

    con.close()
    path = f'{DIR}/{FOLDER}/{file_name}'
    mixwallpaper(path)


class qt(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(1000, 300, 800, 500)
        self.setWindowTitle("Прогноз обоев")

        self.today_btn = QPushButton("Погода на данный момент", self)
        self.today_btn.resize(200, 60)
        self.today_btn.move(540, 150)
        self.today_btn.clicked.connect(self.today_output)

        self.forecast_btn = QPushButton("Прогноз на ближайшие 15 часов", self)
        self.forecast_btn.resize(200, 60)
        self.forecast_btn.move(540, 250)
        self.forecast_btn.clicked.connect(self.forecast_output)

        self.oboi_btn = QPushButton("Поменять обои", self)
        self.oboi_btn.resize(200, 60)
        self.oboi_btn.move(540, 350)
        self.oboi_btn.clicked.connect(self.change_photo)

        self.weather_today_nadpis = QLabel("Данные о погоде на сегодня", self)
        self.weather_today_nadpis.resize(200, 100)
        self.weather_today_nadpis.move(30, 70)

        self.weather_today_weather = QLabel(self)
        self.weather_today_weather.resize(100, 30)
        self.weather_today_weather.move(30, 135)

        self.weather_today_temp = QLabel(self)
        self.weather_today_temp.resize(100, 30)
        self.weather_today_temp.move(30, 155)

        self.weather_today_temp_max = QLabel(self)
        self.weather_today_temp_max.resize(200, 30)
        self.weather_today_temp_max.move(30, 175)

        self.weather_today_temp_min = QLabel(self)
        self.weather_today_temp_min.resize(200, 30)
        self.weather_today_temp_min.move(30, 195)

        self.weather_today_wind_speed = QLabel(self)
        self.weather_today_wind_speed.resize(150, 30)
        self.weather_today_wind_speed.move(30, 215)

        self.weather_today_humidity = QLabel(self)
        self.weather_today_humidity.resize(150, 30)
        self.weather_today_humidity.move(30, 235)

        self.weather_today_sunrise = QLabel(self)
        self.weather_today_sunrise.resize(200, 30)
        self.weather_today_sunrise.move(30, 255)

        self.weather_today_sunset = QLabel(self)
        self.weather_today_sunset.resize(200, 30)
        self.weather_today_sunset.move(30, 275)

        self.forecast_label = QLabel(
            "Прогноз погоды на ближайшие 15 часов", self)
        self.forecast_label.resize(300, 100)
        self.forecast_label.move(250, 70)

        self.forecast1 = QLabel(self)
        self.forecast1.resize(300, 30)
        self.forecast1.move(250, 145)

        self.forecast2 = QLabel(self)
        self.forecast2.resize(300, 30)
        self.forecast2.move(250, 165)

        self.forecast3 = QLabel(self)
        self.forecast3.resize(300, 30)
        self.forecast3.move(250, 185)

        self.forecast4 = QLabel(self)
        self.forecast4.resize(300, 30)
        self.forecast4.move(250, 205)

        self.forecast5 = QLabel(self)
        self.forecast5.resize(300, 30)
        self.forecast5.move(250, 225)

        self.input_label = QLabel("Введите город:", self)
        self.input_label.resize(100, 40)
        self.input_label.move(260, 30)

        self.input_pole = QLineEdit(self)
        self.input_pole.setPlaceholderText("Москва")

        self.input_pole.resize(130, 20)
        self.input_pole.move(342, 40)

    def today_output(self):
        """ Вывод данных о погоде на данный момент """
        global weather
        value = self.input_pole.text()
        if value:
            weather = pogoda.Weather_today(value)
        else:
            weather = pogoda.Weather_today()
        rus_weather = ''
        if weather.weather == 'Clouds':
            rus_weather = "Облачно"
        elif weather.weather == 'Clear':
            rus_weather = 'Ясно'
        elif weather.weather == 'Snow':
            rus_weather = 'Снег'
        elif weather.weather == 'Rain':
            rus_weather = 'Дождь'
        elif weather.weather == 'Mist' or weather.weather == 'Fog':
            rus_weather = 'Туман'
        wh = f'Погода: {rus_weather}'
        te = f'Температура: {weather.temp}'
        tx = f'Максимальная температура: {weather.temp_max}'
        tn = f'Минимальная температура: {weather.temp_max}'
        ws = f'Скорость ветра: {weather.wind_speed}'
        hm = f'Влажность: {weather.humidity}'
        sr = f'Восход солнца(по Мск времени):{weather.sunrise}'
        ss = f'Заход солнца(по Мск времени):{weather.sunset}'
        self.weather_today_weather.setText(wh)
        self.weather_today_temp.setText(te)
        self.weather_today_temp_max.setText(tx)
        self.weather_today_temp_min.setText(tn)
        self.weather_today_wind_speed.setText(ws)
        self.weather_today_humidity.setText(hm)
        self.weather_today_sunrise.setText(sr)
        self.weather_today_sunset.setText(ss)
        print(weather.weather)

    def forecast_output(self):
        """ Вывод прогноза погоды на ближайшие 15 часов """
        value = self.input_pole.text()
        if value:
            self.forecast = pogoda.Forecast(value)
        else:
            self.forecast = pogoda.Forecast()
        li = self.forecast.get_list()
        a = tuple(map(str, li[0]))
        b = tuple(map(str, li[1]))
        c = tuple(map(str, li[2]))
        d = tuple(map(str, li[3]))
        e = tuple(map(str, li[4]))
        self.forecast1.setText(', '.join(a))
        self.forecast2.setText(', '.join(b))
        self.forecast3.setText(', '.join(c))
        self.forecast4.setText(', '.join(d))
        self.forecast5.setText(', '.join(e))

    def change_photo(self):
        """ Смена картинки рабочего стола, в зависимости от данных о погоде"""
        change_theme()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app_icon = QtGui.QIcon("photo_img/favicon.ico")
    app.setWindowIcon(app_icon)
    ex = qt()
    ex.show()
    sys.exit(app.exec())
