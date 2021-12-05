from typing import Final

from requests import post as request_post

from loader import logger_guru



def synthesize_voice_by_ya(FOLDER_ID: str, API_YA_TTS: str, text: str) -> bytes:
    """
    Here we translate the text into voice using Yandex TTS API
    :param FOLDER_ID: cloud folder
    :param API_YA_TTS: api key
    :param text: text to convert
    :return: bytes-object (.ogg)
    """
    url: Final[str] = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
    headers: dict = {'Authorization': f'Api-key {API_YA_TTS}'}
    data: dict = {
        'text': text,
        'folderId': FOLDER_ID,
        'voice': 'alena',
        'speed': '0.9',
    }
    try:
        with request_post(url, headers=headers, data=data, stream=True) as resp:
            if resp.status_code != 200:
                raise RuntimeError(f"Invalid response received: {resp.status_code=}, {resp.text=}")
            get_data: bytes = resp.content
        return get_data
    except RuntimeError as err:
        logger_guru.warning(f'{repr(err)} : Error in synthesize_voice_by_ya.')