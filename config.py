from os import getenv

from dotenv import load_dotenv
load_dotenv()

time_zone: str = getenv('TIMEZONE')

BOT_TOKEN: str = getenv('BOT_TOKEN')

admins_bot: dict = {
    'creator': getenv('creator'),
    'assistant': getenv('assistant'),
}

DB_NAME: str = getenv('DB_NAME')

HOST_REDIS: str = getenv('HOST_REDIS')
PORT_REDIS: str = getenv('PORT_REDIS')
PASS_REDIS: str = getenv('PASS_REDIS')

redis_for_bot: dict = {
    'host': HOST_REDIS,
    'port': PORT_REDIS,
    'password': PASS_REDIS,
    'prefix': 'fsm_key'
}
redis_data_cache: dict = {
    'url': f'redis://{HOST_REDIS}',
    'password': PASS_REDIS,
    'db': 1
}

WEBAPP_HOST: str = getenv('WEBAPP_HOST')
WEBAPP_PORT: int = 3001
WEBHOOK_HOST: str = getenv('WEBHOOK_HOST')
WEBHOOK_PATH: str = getenv('WEBHOOK_PATH')
WEBHOOK_URL: str = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

HORO_XML: str = getenv('HORO_XML')
HAIRCUT_PARSE: str = getenv('HAIRCUT_PARSE')

API_WEATHER: str = getenv('API_WEATHER')
API_WEATHER2: str = getenv('API_WEATHER2')
CITY_WEATHER: str = getenv('CITY_WEATHER')

FOLDER_ID: str = getenv('FOLDER_ID')
API_YA_STT: str = getenv('API_YA_STT')
API_YA_TTS: str = getenv('API_YA_TTS')

OCR_URL: str = getenv('OCR_URL')
