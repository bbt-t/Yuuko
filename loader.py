from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger as logger_guru

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine

from config import BOT_TOKEN, redis, DB_NAME




storage = RedisStorage2(**redis)
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

scheduler = AsyncIOScheduler()
scheduler.configure(
    jobstores={'default': SQLAlchemyJobStore(url='sqlite:///data/jobs.sqlite')},
    logger=logger_guru)

# SQLite:
# db = Database()

# SQLite with aiosqlite and async_sqlalchemy
Base = declarative_base()
engine = create_async_engine(f'sqlite+aiosqlite:///data/{DB_NAME}')

logger_guru.add(
    'logging-bot-home.log',
    format='{time} {level} {message}',
    level='WARNING',
    rotation='00:00',
    compression='gz',
    )