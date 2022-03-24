from datetime import timedelta
from typing import Literal, Optional
from xml.etree.ElementTree import fromstring as ElementTree_fromstring

from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiohttp import ClientSession
from aioredis import from_url as aioredis_from_url
from bs4 import BeautifulSoup

from config import bot_config
from loader import logger_guru, dp
from utils.misc.other_funcs import get_time_now


async def get_user_horoscope_ru(zodiac: str, when: Literal['today', 'tomorrow']) -> Optional[str]:
    """
    Parsing XML horoscope by parameters.
    :param zodiac: chosen zodiac
    :param when: horoscope for today or tomorrow
    :return: horoscope-string
    """
    async def get_horoscope() -> Optional[str]:
        async with ClientSession() as session:
            async with session.get(bot_config.work_with_api.other.HORO_XML) as resp:
                if resp.status != 200:
                    logger_guru.warning(f"{resp.status=} : Bad request!")
                    raise ConnectionError

                tree = ElementTree_fromstring(await resp.text())
        return ''.join(
            msg.text for msg in (chunk.findall(when)[0] for chunk in tree.findall(zodiac))
        )
    if not isinstance(dp.storage, RedisStorage2):
        generated_msg: str = await get_horoscope()
    else:
        async with aioredis_from_url(**bot_config.redis.redis_data_cache.as_dict()) as connect_redis:
            if data := await connect_redis.hget(name='horoscope', key=f'ru_{zodiac}_{when}'):
                generated_msg: str = data.decode()
            else:
                generated_msg: str = await get_horoscope()
                await connect_redis.hset(name='horoscope', key=f'ru_{zodiac}_{when}', value=generated_msg)
    return generated_msg


async def get_user_horoscope_en(zodiac: str, when: Literal['today', 'tomorrow']) -> Optional[str]:
    """
    Parsing XML horoscope by parameters.
    :param zodiac: chosen zodiac
    :param when: horoscope for today or tomorrow
    :return: horoscope-string
    """
    match when:
        case 'today':
            date: str = get_time_now(bot_config.time_zone).strftime('%Y%m%d')
        case 'tomorrow':
            date: str = (get_time_now(bot_config.time_zone) + timedelta(days=1)).strftime('%Y%m%d')

    async def get_horoscope() -> Optional[str]:
        async with ClientSession() as session:
            async with session.get(
                    f"{bot_config.work_with_api.other.HORO_EN}{zodiac}/daily-{date}.html"
            ) as resp:
                if resp.status != 200:
                    logger_guru.warning(f"{resp.status=} : Bad request!")
                    raise ConnectionError
                soup = BeautifulSoup(await resp.text(), 'lxml')

        return soup.find(class_="Fz(13px) Lh(1.9) Whs(n) C($c-fuji-batcave)").get_text().replace(
            "Discover why 2022 is the year you've been waiting for with your 2022 Premium Horoscope.", ''
        )
    if not isinstance(dp.storage, RedisStorage2):
        generated_msg: str = await get_horoscope()
    else:
        async with aioredis_from_url(**bot_config.redis.redis_data_cache.as_dict()) as connect_redis:
            if data := await connect_redis.hget(name='horoscope', key=f'en_{zodiac}_{when}'):
                generated_msg: str = data.decode()
            else:
                generated_msg: str = await get_horoscope()
                await connect_redis.hset(name='horoscope', key=f'en_{zodiac}_{when}', value=generated_msg)
    return generated_msg
