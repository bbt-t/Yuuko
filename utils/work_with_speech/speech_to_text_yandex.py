from aiohttp import ClientSession

from loader import logger_guru
from utils.enums_data import ApiInfo




async def recognize_speech_by_ya(msg: bytes, FOLDER_ID: str, API_YA_STT: str) -> str:
    """
    We recognize the voice by means of the Yandex Speech API service.
    :param msg: voice message
    :param FOLDER_ID: your cloud name Yandex
    :param API_YA_STT: API key
    :return: what recognized
    """
    url: str = ApiInfo.STT_YANDEX.value
    headers: dict = {'Authorization': f'Api-Key {API_YA_STT}'}
    params: dict = {
        'topic': 'general',
        'folderId': FOLDER_ID,
        'lang': 'ru-RU'
    }
    try:
        async with ClientSession() as session:
            async with session.post(url=url, headers=headers, data=msg, params=params) as resp:
                result = await resp.json()
        text: str = result.get('result')
        return text
    except:
        logger_guru.warning('BAD REQUEST : Error in Yandex STT func')
