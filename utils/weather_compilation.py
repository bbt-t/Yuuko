from math import ceil
from typing import Final

from aiohttp import ClientSession
from aioredis import from_url as aioredis_from_url

from config import CITY_WEATHER, time_now, redis_for_data
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

    async with aioredis_from_url(**redis_for_data) as connect_redis:
        if data := await connect_redis.get(f'weather_cache_{time_now.date()}'):
            generated_msg: str = data.decode()
        else:
            try:
                async with ClientSession() as session:
                    async with session.get(URL[0]) as resp:
                        req = await resp.json()

                temp: int = ceil(req['main']['temp_min'])
                wind: float = req['wind']['speed']
                weather: str = req['weather'][0]['description']
                weather_main: str = req['weather'][0]['main']
            except:
                logger_guru.warning("Main API didn't work !")
                async with ClientSession() as session:
                    async with session.get(
                        f'http://dataservice.accuweather.com/locations/v1/cities/autocomplete?apikey='
                        f'{api_key_2}&q={city}') as resp_city:
                        city_spare_api: str = (await resp_city.json())[0]['Key']

                    async with session.get(URL[1].replace('CITY', city_spare_api)) as resp:
                        req = await resp.json()

                temp: int = ceil(req['DailyForecasts'][0]['RealFeelTemperature']['Maximum']['Value'])
                wind: float = req['DailyForecasts'][0]['Day']['Wind']['Speed']['Value']
                weather: str = req['DailyForecasts'][0]['Day']['ShortPhrase']
                weather_main: str = ''

                if req['DailyForecasts'][0]['Day']['ThunderstormProbability'] >= 40:
                    weather_main: str = 'thunderstorm'
                if req['DailyForecasts'][0]['Day']['RainProbability'] >= 40:
                    weather_main: str = 'rain'

            if 4 <= temp <= 10:
                rep_temp: str = 'Относительно холодно'
            elif temp <= 3:
                rep_temp: str = 'Холодно! одевайся потеплее!'
            else:
                rep_temp: str = 'Тепло, хорошо ! прекрасный тёплый день :)'

            if wind <= 5:
                rep_wind: str = 'не страшно :)'
            elif 5 < wind < 15:
                rep_wind: str = 'Ветер ощущется! Желательно надеть шарф!'
            else:
                rep_wind: str = 'Штормовой ветрище! Необходимо защититься от ветра и быть осторожным!'

            generated_msg = (
                f"Сегодня будет <CODE>{weather.upper()}</CODE> , <CODE>{temp}</CODE> градусов,\n<b>{rep_temp}</b>\n"
                f"Скорость ветра <CODE>{wind}</CODE> м/с,\n{rep_wind}\n"
                f"{'<b>НЕ ЗАБУДЬ ВЗЯТЬ ЗОНТ !</b>' if any(x in weather_main.lower() for x in ('rain', 'thunderstorm')) else ''}"
            )
            await connect_redis.setex(f'weather_cache_{time_now.date()}', 7200, generated_msg)

    return generated_msg

