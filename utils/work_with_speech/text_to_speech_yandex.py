from typing import Final

from aiohttp import ClientSession

from loader import logger_guru




async def synthesize_voice_by_ya(FOLDER_ID: str, API_YA_TTS: str, text: str) -> bytes:
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
        'speed': '0.8',
    }
    try:
        async with ClientSession() as session:
            async with session.post(url=url, headers=headers, data=data) as resp:
                result: bytes = await resp.read()
        return result
    except RuntimeError as err:
        logger_guru.warning(f'{repr(err)} : Error in synthesize_voice_by_ya.')
