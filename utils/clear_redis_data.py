from aioredis import from_url as aioredis_from_url

from config import redis_for_data


async def clear_redis() -> None:
    async with aioredis_from_url(**redis_for_data) as connect:
        await connect.flushdb()
