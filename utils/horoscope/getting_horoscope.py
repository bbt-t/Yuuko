from typing import Literal
from xml.etree.ElementTree import fromstring as ElementTree_fromstring

from requests import get as requests_get

from config import HORO_XML




async def get_user_horoscope(zodiac: str, when: Literal['today', 'tomorrow']) -> str:
    """
    Parsing XML horoscope by parameters.
    :param zodiac: chosen zodiac
    :param when: horoscope for today or tomorrow
    :return: horoscope-string
    """
    req = requests_get(HORO_XML)
    tree = ElementTree_fromstring(req.content)
    generated_msg: str = ''.join(
        msg.text for msg in (x.findall(when)[0] for x in tree.findall(zodiac))
    )
    return generated_msg
