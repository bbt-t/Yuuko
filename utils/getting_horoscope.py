from datetime import timedelta
from typing import Literal
from xml.etree.ElementTree import fromstring as ElementTree_fromstring

from aiohttp import ClientSession
from aioredis import from_url as aioredis_from_url
from bs4 import BeautifulSoup

from config import redis_data_cache, work_with_api, time_zone
from loader import logger_guru
from utils.misc.other_funcs import get_time_now


async def get_user_horoscope_ru(zodiac: str, when: Literal['today', 'tomorrow']) -> str:
    """
    Parsing XML horoscope by parameters.
    :param zodiac: chosen zodiac
    :param when: horoscope for today or tomorrow
    :return: horoscope-string
    """
    async with aioredis_from_url(**redis_data_cache) as connect_redis:

        if data := await connect_redis.get(f'horoscope_ru_{zodiac}_{when}'):
            generated_msg: str = data.decode()
        else:
            async with ClientSession() as session:
                async with session.get(work_with_api['OTHER']['HORO_XML']) as resp:

                    if resp.status != 200:
                        logger_guru.warning(f"{resp.status=} : Bad request!")
                        return 'Что-то пошло не так...попробуй позже.'

                    tree = ElementTree_fromstring(await resp.text())

            generated_msg: str = ''.join(
                msg.text for msg in (chunk.findall(when)[0] for chunk in tree.findall(zodiac))
            )
            await connect_redis.set(f'horoscope_ru_{zodiac}_{when}', generated_msg)

    return generated_msg


async def get_user_horoscope_en(zodiac: str, when: Literal['today', 'tomorrow']) -> str:
    """
    Parsing XML horoscope by parameters.
    :param zodiac: chosen zodiac
    :param when: horoscope for today or tomorrow
    :return: horoscope-string
    """
    match when:
        case 'today':
            date: str = get_time_now(time_zone).strftime('%Y%m%d')
        case 'tomorrow':
            date: str = (get_time_now(time_zone) + timedelta(days=1)).strftime('%Y%m%d')

    async with aioredis_from_url(**redis_data_cache) as connect_redis:

        if data := await connect_redis.get(f'horoscope_en_{zodiac}_{when}'):
            generated_msg: str = data.decode()
        else:
            async with ClientSession() as session:
                async with session.get(f"{work_with_api['OTHER']['HORO_EN']}{zodiac}/daily-{date}.html") as resp:

                    if resp.status != 200:
                        logger_guru.warning(f"{resp.status=} : Bad request!")
                        return 'Что-то пошло не так...попробуй позже.'

                    soup = BeautifulSoup(await resp.text(), 'lxml')

            generated_msg: str = soup.find(class_="Fz(13px) Lh(1.9) Whs(n) C($c-fuji-batcave)").get_text().replace(
                "Discover why 2022 is the year you've been waiting for with your 2022 Premium Horoscope.", ''
            )
            await connect_redis.set(f'horoscope_en_{zodiac}_{when}', generated_msg)

    return generated_msg




