from math import ceil

from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiohttp import ClientSession
from aioredis import from_url as aioredis_from_url

from config import bot_config
from loader import logger_guru, dp
from .misc.enums_data import ApiInfo


async def create_weather_forecast() -> str:
    """
    Weather api request func
    :return: weather for the current hour
    """
    if isinstance(dp. storage, RedisStorage2):
        async with aioredis_from_url(**bot_config.redis.redis_data_cache.as_dict()) as connect_redis:
            if data := await connect_redis.get('weather_cache'):
                return data.decode()

    try:
        req: dict = await get_weather_info()

        temp: int = ceil(req['main']['temp_min'])
        wind: float = ceil(req['wind']['speed'])
        weather: str = req['weather'][0]['description']
        weather_main: str = req['weather'][0]['main']
    except KeyError:
        logger_guru.warning("Main API didn't work !")

        req: dict = await get_weather_info(is_alter=True)

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
        rep_wind: str = 'Ветер ощущается! Желательно надеть шарф!'
    else:
        rep_wind: str = 'Штормовой ветрище! Необходимо защититься от ветра и быть осторожным!'

    take_an_umbrella_with_you: str = (
        '<b>⛈ НЕ ЗАБУДЬ ВЗЯТЬ ЗОНТ ☔</b>'
        if any(x in weather_main.lower() for x in ('rain', 'thunderstorm')) else ''
    )
    generated_msg: str = (
        f"Сегодня будет <CODE>{weather.upper()} {temp}&#176;</CODE>\n<b>{rep_temp}</b>\n"
        f"Скорость ветра <CODE>{wind}</CODE> м/с,\n{rep_wind}\n{take_an_umbrella_with_you}"
    )
    if isinstance(dp.storage, RedisStorage2):
        async with aioredis_from_url(**bot_config.redis.redis_data_cache.as_dict()) as connect_redis:
            await connect_redis.setex('weather_cache', 3600, generated_msg)

    return generated_msg


async def get_weather_info(is_alter: bool = False) -> dict:
    """
    Request to API.
    :param is_alter: request to alternative API
    :return: API answer
    """
    if is_alter:
        async with ClientSession() as session:
            async with session.get(ApiInfo.GET_CITY_ID.value) as resp_city:
                received_city: str = (await resp_city.json())[0]['Key']
            async with session.get(ApiInfo.WEATHER_API_RESERVE.value.replace('CITY', received_city)) as resp:
                result: dict = await resp.json()
    else:
        async with ClientSession() as session:
            async with session.get(ApiInfo.WEATHER_API_BASIC.value) as resp:
                result: dict = await resp.json()
    return result
