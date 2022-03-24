from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aioredis import from_url as aioredis_from_url

from config import bot_config
from loader import dp


async def clear_redis() -> None:
    """
    Deletes all keys in the redis-db.
    """
    if isinstance(dp.storage, RedisStorage2):
        async with aioredis_from_url(**bot_config.redis.redis_data_cache.as_dict()) as connect:
            await connect.flushall()
