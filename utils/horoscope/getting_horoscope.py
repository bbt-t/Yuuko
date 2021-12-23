from typing import Literal
from xml.etree.ElementTree import fromstring as ElementTree_fromstring

from requests import get as requests_get

from config import HORO_XML


zodiac_signs = {
    'овен': 'aries',
    'телец': 'taurus',
    'близнецы': 'gemini',
    'рак': 'cancer',
    'лев': 'leo',
    'дева': 'virgo',
    'весы': 'libra',
    'скорпион': 'scorpio',
    'стрелец': 'sagittarius',
    'козерог': 'capricorn',
    'водолей': 'aquarius',
    'рыбы': 'pisces'
}


async def get_user_horoscope(zodiac: str, when: Literal['today', 'tomorrow'] = 'today') -> str:
    req = requests_get(HORO_XML)
    tree = ElementTree_fromstring(req.content)
    generated_msg: str = ''.join(
        msg.text for msg in (x.findall(when)[0] for x in tree.findall(zodiac_signs[zodiac]))
    )
    return generated_msg
