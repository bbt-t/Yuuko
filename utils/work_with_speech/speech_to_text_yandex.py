from json import loads as json_loads
from typing import Final

from requests import post, exceptions

from loader import logger_guru




def recognize_speech_by_ya(msg: bytes, FOLDER_ID: str, API_YA_STT: str) -> str:
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
        response = post(
            url,
            params=params,
            headers=headers,
            data=msg
        )
        text: str = json_loads(response.content.decode('UTF-8'))['result']
        return text
    except (BaseException, exceptions) as err:
        logger_guru.warning(f'{repr(err)} : Error in Yandex STT func')
        return 'ой :( попробуй позднее...'
