from typing import Final

from httpx import post as httpx_post

from loader import logger_guru




async def recognize_speech_by_ya(msg: bytes, FOLDER_ID: str, API_YA_STT: str) -> str:
    """
    We recognize the voice by means of the Yandex Speech API service.
    :param msg: voice message
    :param FOLDER_ID: your cloud name Yandex
    :param API_YA_STT: API key
    :return: what recognized
    """
    url: Final[str] = 'https://stt.api.cloud.yandex.net/speech/v1/stt:recognize'
    headers: dict = {'Authorization': f'Api-Key {API_YA_STT}'}
    params: dict = {
        'topic': 'general',
        'folderId': FOLDER_ID,
        'lang': 'ru-RU'
    }
    try:
        response = httpx_post(url=url, headers=headers, content=msg, params=params)
        text: str = response.json()['result']

        return text
    except:
        logger_guru.warning('BAD REQUEST : Error in Yandex STT func')
