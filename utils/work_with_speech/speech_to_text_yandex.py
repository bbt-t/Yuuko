from typing import Optional

from aiohttp import ClientSession

from loader import logger_guru
from ..misc.enums_data import ApiInfo


async def recognize_speech_by_ya(msg: bytes, folder_id: str, api_ya_stt: str) -> Optional[str]:
    """
    We recognize the voice by means of the Yandex Speech API service.
    :param msg: voice message
    :param folder_id: your cloud name Yandex
    :param api_ya_stt: API key
    :return: what recognized
    """
    url: str = ApiInfo.STT_YANDEX.value
    headers: dict = {'Authorization': f'Api-Key {api_ya_stt}'}
    params: dict = {
        'topic': 'general',
        'folderId': folder_id,
        'lang': 'ru-RU'
    }
    try:
        async with ClientSession() as session:
            async with session.post(url=url, headers=headers, data=msg, params=params) as resp:
                if resp.status == 200:
                    result: dict = await resp.json()
                    return result.get('result')
    except Exception as err:
        logger_guru.warning(f'{repr(err)} : Error in Yandex STT func')
