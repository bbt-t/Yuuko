from aiohttp import ClientSession

from loader import logger_guru
from ..misc.enums_data import ApiInfo


async def synthesize_voice_by_ya(FOLDER_ID: str, API_YA_TTS: str, text: str, lang: str) -> bytes:
    """
    Here we translate the text into voice using Yandex TTS API
    :param FOLDER_ID: cloud folder
    :param API_YA_TTS: api key
    :param text: text to convert
    :return: bytes-object (.ogg)
    """
    translate_table = {'ru': 'ru-RU', 'en': 'en-US'}
    lang_tranl: str = ''.join(val for key, val in translate_table.items() if key == lang)

    url: str = ApiInfo.TTS_YANDEX.value
    headers: dict = {'Authorization': f'Api-key {API_YA_TTS}'}
    data: dict = {
        'lang': lang_tranl,
        'text': text,
        'folderId': FOLDER_ID,
        'voice': 'alena' if lang == 'ru' else 'oksana',
        'speed': '0.8',
    }
    try:
        async with ClientSession() as session:
            async with session.post(url=url, headers=headers, data=data) as resp:
                result: bytes = await resp.read()
        return result
    except BaseException as err:
        logger_guru.warning(f'{repr(err)} : Error in synthesize_voice_by_ya.')
