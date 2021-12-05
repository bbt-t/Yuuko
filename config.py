from datetime import datetime
from enum import IntEnum, unique
from os import getenv
import pytz

from dotenv import load_dotenv
load_dotenv()




@unique
class AdminsBot(IntEnum):
    creator = getenv('creator')
    assistant = getenv('assistant')


BOT_TOKEN = getenv('BOT_TOKEN')

API_WEATHER = getenv('API_WEATHER')
API_WEATHER2 = getenv('API_WEATHER2')
CITY_WEATHER = getenv('CITY_WEATHER')

pkl_key = getenv('PKL_KEY')

FOLDER_ID = getenv('FOLDER_ID')
API_YA_STT = getenv('API_YA_STT')
API_YA_TTS = getenv('API_YA_TTS')

timezone = getenv('TIMEZONE')
time_zone = pytz.timezone(timezone)
time_now = time_zone.localize(datetime.now())