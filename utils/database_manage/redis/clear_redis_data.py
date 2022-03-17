from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aioredis import from_url as aioredis_from_url

from config import redis_data_cache
from loader import dp


async def clear_redis() -> None:
    """
    Deletes all keys in the redis-db.
    """
    if isinstance(dp.storage, RedisStorage2):
        async with aioredis_from_url(**redis_data_cache) as connect:
            await connect.flushall()
