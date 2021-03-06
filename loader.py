from asyncio import set_event_loop_policy

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
from uvloop import EventLoopPolicy as uvloop_Loop

from config import bot_config
from loguru import logger as logger_guru


set_event_loop_policy(uvloop_Loop())


storage = RedisStorage2(**bot_config.redis.redis_for_bot.as_dict())
bot = Bot(token=bot_config.BOT_TOKEN, parse_mode=types.ParseMode.HTML, connections_limit=100)
dp = Dispatcher(bot, storage=storage)

scheduler = AsyncIOScheduler()
scheduler.configure(
    jobstores={'default': SQLAlchemyJobStore(url='sqlite:///data/db/jobs.sqlite')},
    logger=logger_guru)

Base = declarative_base()
engine = create_async_engine('sqlite+aiosqlite:///data/db/sql_db_bot.db', future=True)

logger_guru.add(
    'data/logs/logging-bot.log',
    format='<red>{time}</red> {level} <level>{message}</level>',
    level='WARNING',
    rotation='00:00',
    compression='gz',
    colorize=True,
    )
