from math import ceil
from typing import Final

from httpx import AsyncClient

from config import CITY_WEATHER
from loader import logger_guru




async def create_weather_forecast(api_key_1: str, api_key_2: str, city: str = CITY_WEATHER) -> str:
    """
    Weather api request func
    :param city: city
    :param api_key: api keys
    """
    URL: Final[tuple] = (f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid='
                         f'{api_key_1}&units=metric&lang=ru',
                         f"http://dataservice.accuweather.com/forecasts/v1/daily/1day/CITY?apikey="
                         f"{api_key_2}&language=ru-ru&metric=true&details=true"
                         )
    try:
        async with AsyncClient() as request:
            req = await request.get(URL[0])
        req = req.json()

        temp: int = ceil(req['main']['temp_min'])
        wind: float = req['wind']['speed']
        weather: str = req['weather'][0]['description']
        weather_main: str = req['weather'][0]['main']
    except:
        logger_guru.warning("Main API didn't work !")

        async with AsyncClient() as request:
            city_spare_api: str = request.get(
                f'http://dataservice.accuweather.com/locations/v1/cities/autocomplete?apikey='
                f'{api_key_2}&q={city}').json()[0]['Key']
            req = await request.get(URL[1].replace('CITY', city_spare_api)).json()

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

    return (
        f"Сегодня будет <CODE>{weather.upper()}</CODE> , <CODE>{temp}</CODE> градусов,\n<b>{rep_temp}</b>\n"
        f"Скорость ветра <CODE>{wind}</CODE> м/с,\n{rep_wind}\n"
        f"{'<b>НЕ ЗАБУДЬ ВЗЯТЬ ЗОНТ !</b>' if any(x in weather_main.lower() for x in ('rain', 'thunderstorm')) else ''}"
    )