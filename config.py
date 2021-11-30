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
city = getenv('city')

pkl_key = getenv('PKL_KEY')

timezone = getenv('TIMEZONE')
time_zone = pytz.timezone(timezone)
time_now = time_zone.localize(datetime.now())



