import json

from requests import post, exceptions

from loader import logger_guru




def recognize_speech_by_Ya(msg: bytes, FOLDER_ID: str, API_YA_STT: str) -> str:
    url: str = 'https://stt.api.cloud.yandex.net/speech/v1/stt:recognize'

    headers: dict = {'Authorization': f'Api-Key {API_YA_STT}'}
    data: dict = {
        'topic': 'general',
        'folderId': FOLDER_ID,
        'lang': 'ru-RU'
    }
    try:
        response = post(
            url,
            params=data,
            headers=headers,
            data=msg
        )
        text: str = json.loads(response.content.decode('UTF-8'))['result']
        return text
    except (BaseException, exceptions) as err:
        logger_guru.warning(f'{err} : Error in Yandex STT func')
        return 'ой :( попробуй позднее...'
