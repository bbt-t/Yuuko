from asyncio import set_event_loop_policy, get_running_loop
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from datetime import datetime
from zoneinfo import ZoneInfo

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
from uvloop import EventLoopPolicy as uvloop_Loop

from config import BOT_TOKEN, redis_for_bot, DB_NAME
from loguru import logger as logger_guru


set_event_loop_policy(uvloop_Loop())

storage = RedisStorage2(**redis_for_bot)
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


def get_time_now(tz: str):
    """
    Take time and date in the time-zone.
    :param tz: time-zone
    :return: datatime object
    """
    zone = ZoneInfo(tz)
    return datetime.now(tz=zone)


async def blocking_io_run_func(func, *args):
    """
    Run in a custom thread pool (IO).
    :param func: func to run in the pool
    :param args: func arguments
    :return: func result
    """
    loop = get_running_loop()
    with ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, func, *args)
    return result


async def cpu_bound_run_func(func, *args):
    """
    Run in a custom process pool (CPU-bound operations).
    :param func: func to run in the pool
    :param args: func arguments
    :return: func result
    """
    loop = get_running_loop()
    with ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, func, *args)
    return result
