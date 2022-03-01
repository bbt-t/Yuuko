from math import ceil

from aiohttp import ClientSession
from aioredis import from_url as aioredis_from_url

from config import redis_data_cache
from loader import logger_guru
from .misc.enums_data import ApiInfo


async def create_weather_forecast() -> str:
    """
    Weather api request func
    :return: weather for the current hour
    """
    async with aioredis_from_url(**redis_data_cache) as connect_redis:
        if data := await connect_redis.get('weather_cache'):
            generated_msg: str = data.decode()
        else:
            try:
                async with ClientSession() as session:
                    async with session.get(ApiInfo.WEATHER_API_BASIC.value) as resp:
                        req = await resp.json()

                temp: int = ceil(req['main']['temp_min'])
                wind: float = ceil(req['wind']['speed'])
                weather: str = req['weather'][0]['description']
                weather_main: str = req['weather'][0]['main']
            except:
                logger_guru.warning("Main API didn't work !")
                req = await accesses_fallback_api()

                temp: int = ceil(req['DailyForecasts'][0]['RealFeelTemperature']['Maximum']['Value'])
                wind: float = ceil(req['DailyForecasts'][0]['Day']['Wind']['Speed']['Value'])
                weather: str = req['DailyForecasts'][0]['Day']['ShortPhrase']
                weather_main: str = ''

                if req['DailyForecasts'][0]['Day']['ThunderstormProbability'] >= 40:
                    weather_main: str = 'thunderstorm'
                if req['DailyForecasts'][0]['Day']['RainProbability'] >= 40:
                    weather_main: str = 'rain'

            if 4 <= temp <= 10:
                rep_temp: str = 'Относительно холодно ❄'
            elif temp <= 3:
                rep_temp: str = 'Холодно! ❄ одевайся потеплее!'
            else:
                rep_temp: str = 'Тепло, хорошо ! прекрасный тёплый день 🌞'

            if wind <= 5:
                rep_wind: str = 'не страшно :)'
            elif 5 < wind < 15:
                rep_wind: str = 'Ветер ощущется! Желательно надеть шарф!'
            else:
                rep_wind: str = 'Штормовой ветрище! Необходимо защититься от ветра и быть осторожным!'

            generated_msg: str = (
                f"Сегодня будет <CODE>{weather.upper()} {temp}&#176;</CODE>\n<b>{rep_temp}</b>\n"
                f"Скорость ветра <CODE>{wind}</CODE> м/с,\n{rep_wind}\n"
                f"{'<b>⛈ НЕ ЗАБУДЬ ВЗЯТЬ ЗОНТ ☔</b>' if any(x in weather_main.lower() for x in ('rain', 'thunderstorm')) else ''}"
            )
            await connect_redis.setex('weather_cache', 3600, generated_msg)

    return generated_msg


async def accesses_fallback_api():
    async with ClientSession() as session:
        async with session.get(ApiInfo.GET_CITY_ID.value) as resp_city:
            received_city: str = (await resp_city.json())[0]['Key']

        async with session.get(ApiInfo.WEATHER_API_RESERVE.value.replace('CITY', received_city)) as resp:
            result = await resp.json()

    return result
