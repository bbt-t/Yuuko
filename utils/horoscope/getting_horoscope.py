from typing import Literal
from xml.etree.ElementTree import fromstring as ElementTree_fromstring

from aiohttp import ClientSession
from aioredis import from_url as aioredis_from_url

from config import HORO_XML, redis_for_data
from loader import logger_guru




async def get_user_horoscope(zodiac: str, when: Literal['today', 'tomorrow']) -> str:
    """
    Parsing XML horoscope by parameters.
    :param zodiac: chosen zodiac
    :param when: horoscope for today or tomorrow
    :return: horoscope-string
    """
    async with aioredis_from_url(**redis_for_data) as connect_redis:

        if data := await connect_redis.get(f'horoscope_{zodiac}_{when}'):
            generated_msg: str = data.decode()
        else:
            async with ClientSession() as session:
                async with session.get(HORO_XML) as resp:

                    if resp.status != 200:
                        logger_guru.warning(f"{resp.status=} : Bad request!")
                        return 'Что-то пошло не так...попробуй позже.'

                    tree = ElementTree_fromstring(await resp.text())

            generated_msg: str = ''.join(
                msg.text for msg in (chunk.findall(when)[0] for chunk in tree.findall(zodiac))
            )
            await connect_redis.set(f'horoscope_{zodiac}_{when}', generated_msg)

    return generated_msg
