from os import getenv

from dotenv import load_dotenv
load_dotenv()


admins_bot: dict = {
    'creator': getenv('creator'),
    'assistant': getenv('assistant'),
}

BOT_TOKEN = getenv('BOT_TOKEN')

API_WEATHER = getenv('API_WEATHER')
API_WEATHER2 = getenv('API_WEATHER2')
CITY_WEATHER = getenv('CITY_WEATHER')

FOLDER_ID = getenv('FOLDER_ID')
API_YA_STT = getenv('API_YA_STT')
API_YA_TTS = getenv('API_YA_TTS')

time_zone = getenv('TIMEZONE')

HOST_REDIS = getenv('HOST_REDIS')

PORT_REDIS = getenv('PORT_REDIS')
PASS_REDIS = getenv('PASS_REDIS')

redis = {
    'host': HOST_REDIS,
    'port': PORT_REDIS,
    'password': PASS_REDIS,
    'prefix': 'fsm_key'
}
redis_data_cache = {
    'url': f'redis://{HOST_REDIS}',
    'password': PASS_REDIS,
    'db': 1
}

DB_NAME = getenv('DB_NAME')

HORO_XML = getenv('HORO_XML')
HAIRCUT_PARSE = getenv('HAIRCUT_PARSE')


WEBAPP_HOST = getenv('WEBAPP_HOST')
WEBAPP_PORT = 3001

WEBHOOK_HOST = getenv('WEBHOOK_HOST')
WEBHOOK_PATH = getenv('WEBHOOK_PATH')
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

OCR_URL = getenv('OCR_URL')
