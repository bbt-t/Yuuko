from os import getenv

from dotenv import load_dotenv
load_dotenv()

time_zone: str = getenv('TIMEZONE')

BOT_TOKEN: str = getenv('BOT_TOKEN')

DB_NAME: str = getenv('DB_NAME')

admins_bot: dict = {
    'creator': getenv('creator'),
    'assistant': getenv('assistant'),
}

redis_for_bot: dict = {
    'host': getenv('HOST_REDIS'),
    'port': getenv('PORT_REDIS'),
    'password': getenv('PASS_REDIS'),
    'prefix': 'fsm_key'
}
redis_data_cache: dict = {
    'url': f"redis://{getenv('HOST_REDIS')}",
    'password': getenv('PASS_REDIS'),
    'db': 1
}

hook_info: dict = {
    'WEBHOOK': {
        'webhook_path': getenv('WEBHOOK_PATH'),
        'host': getenv('WEBAPP_HOST'),
        'port': 3001
    },
    'WEBHOOK_URL': f"{getenv('WEBHOOK_HOST')}{getenv('WEBHOOK_PATH')}"
}

work_with_api: dict = {
    'YANDEX': {
        'FOLDER_ID': getenv('FOLDER_ID'),
        'API_YA_STT': getenv('API_YA_STT'),
        'API_YA_TTS': getenv('API_YA_TTS')
    },
    'WEATHER': {
        'API_WEATHER': getenv('API_WEATHER'),
        'API_WEATHER2': getenv('API_WEATHER2'),
        'CITY_WEATHER': getenv('CITY_WEATHER'),
    },
    'OTHER': {
        'HORO_XML': getenv('HORO_XML'),
        'HAIRCUT_PARSE': getenv('HAIRCUT_PARSE'),
        'OCR_URL': getenv('OCR_URL'),
    }
}

# HORO_XML: str = getenv('HORO_XML')
# HAIRCUT_PARSE: str = getenv('HAIRCUT_PARSE')
#
# API_WEATHER: str = getenv('API_WEATHER')
# API_WEATHER2: str = getenv('API_WEATHER2')
# CITY_WEATHER: str = getenv('CITY_WEATHER')
#
# FOLDER_ID: str = getenv('FOLDER_ID')
# API_YA_STT: str = getenv('API_YA_STT')
# API_YA_TTS: str = getenv('API_YA_TTS')
#
# OCR_URL: str = getenv('OCR_URL')