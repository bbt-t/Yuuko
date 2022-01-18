from aioredis import from_url as aioredis_from_url

from config import redis_data_cache


async def clear_redis() -> None:
    """
    Deletes all keys in the redis-db.
    """
    async with aioredis_from_url(**redis_data_cache) as connect:
        await connect.flushall()
