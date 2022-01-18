from asyncio import set_event_loop_policy as asyncio_set_event_loop_policy
from datetime import datetime
from zoneinfo import ZoneInfo

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
from uvloop import EventLoopPolicy as uvloop_Loop

from config import BOT_TOKEN, redis, DB_NAME
from loguru import logger as logger_guru


asyncio_set_event_loop_policy(uvloop_Loop())

storage = RedisStorage2(**redis)
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

scheduler = AsyncIOScheduler()
scheduler.configure(
    jobstores={'default': SQLAlchemyJobStore(url='sqlite:///data/jobs.sqlite')},
    logger=logger_guru)

Base = declarative_base()
engine = create_async_engine(f'sqlite+aiosqlite:///data/{DB_NAME}')

logger_guru.add(
    'data/logs/logging-bot-home.log',
    format='{time} {level} {message}',
    level='WARNING',
    rotation='00:00',
    compression='gz',
    )


def get_time_now(tz):
    zone = ZoneInfo(tz)
    return datetime.now(tz=zone)
