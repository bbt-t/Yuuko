from math import ceil
from requests import get as request_get
from typing import Final

from aiogram.types import ParseMode

from config import API_WEATHER, API_WEATHER2, city
from loader import bot, logger_guru




@logger_guru.catch()
def report_weather(city: str, api_key_1: str, api_key_2: str) -> str:
    """
    Weather api request func
    :param city: city
    :param api_key: api keys
    """
    URL: Final[tuple] = (
        f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key_1}&units=metric&lang=ru',
        f'http://dataservice.accuweather.com/forecasts/v1/daily/1day/293686?{api_key_2}&language=ru-ru&metric=true&details=true'
    )

    req = request_get(URL[0])
    if req.status_code == 200:
        req = req.json()

        temp: int = ceil(req['main']['temp_min'])
        wind: float = req['wind']['speed']
        weather: str = req['weather'][0]['description']
        weather_main: str = req['weather'][0]['main']
    else:
        req = request_get(URL[1]).json()

        temp: int = ceil(req['DailyForecasts'][0]['RealFeelTemperature']['Maximum']['Value'])
        wind: float = round(req['DailyForecasts'][0]['Day']['Wind']['Speed']['Value'] / 3.6)
        weather: str = req['DailyForecasts'][0]['Day']['ShortPhrase']
        weather_main: str = ''

        if req['DailyForecasts'][0]['Day']['ThunderstormProbability'] >= 40:
            weather_main: str = 'thunderstorm'
        if req['DailyForecasts'][0]['Day']['RainProbability'] >= 40:
            weather_main: str = 'rain'

    if 4 <= temp <= 11:
        rep_temp: str = 'ХОЛОДНО! одевайся потеплее!'
    elif temp <= 3:
        rep_temp: str = 'ОЧЕНЬ холодно! одеться необходимо тепло!'
    else:
        rep_temp: str = 'Тепло, хорошо ! прекрасный тёплый день :)'

    if wind <= 5:
        rep_wind: str = 'не страшно :)'
    elif 5 < wind < 15:
        rep_wind: str = 'Ветер ощущется! Желательно надеть шарф!'
    else:
        rep_wind: str = 'Штормовой ветрище! Необходимо защититься от ветра и быть осторожным!'

    return (f"Сегодня будет <CODE>{weather.upper()}</CODE> , <CODE>{temp}</CODE> градусов,\n<b>{rep_temp}</b>\n"
            f"Скорость ветра <CODE>{wind}</CODE> м/с, {rep_wind}\n"
            f"{'<b>НЕ ЗАБУДЬ ВЗЯТЬ ЗОНТ !</b>' if any(x in weather_main.lower() for x in ('rain', 'thunderstorm')) else ''}")


@logger_guru.catch()
async def send_weather(id: int):
    await bot.send_message(id, report_weather(city, API_WEATHER, API_WEATHER2), ParseMode.HTML)
