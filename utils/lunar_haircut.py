from typing import Optional

from bs4 import BeautifulSoup
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiohttp import ClientSession, http_exceptions
from aioredis import from_url as aioredis_from_url

from config import bot_config
from loader import logger_guru, dp
from utils.misc.other_funcs import get_time_now


async def lunar_calendar_haircut() -> Optional[str]:
    """
    Forms a list of "favorable" days.
    """
    time = get_time_now(bot_config.time_zone)
    year, month = time.strftime('%Y'), time.strftime('%B').lower()

    async def get_lunar_calendar() -> Optional[str]:
        async with ClientSession() as session:
            async with session.get('{}{}/{}'.format(bot_config.work_with_api.other.HAIRCUT_PARSE, year, month)) as resp:
                if resp.status != 200:
                    logger_guru.warning(f"{resp.status=} : Bad request!")
                    raise http_exceptions.HttpBadRequest
                soup = BeautifulSoup(await resp.text(), 'lxml')

        items = soup.find_all(class_='next_phase month_row green2')
        return ','.join(
            sorted(
                {
                    soup_data.text.split()[0] for soup_data in items
                    if soup_data.find('span', style='font-weight: bold;')
                },
                key=int
            )
        )

    if not isinstance(dp. storage, RedisStorage2):
        text: str = await get_lunar_calendar()
    else:
        async with aioredis_from_url(**bot_config.redis.redis_data_cache.as_dict()) as connect_redis:
            if data := await connect_redis.get('haircut'):
                text: str = data.decode()
            else:
                text: str = await get_lunar_calendar()
                await connect_redis.set('haircut', text)
    return text
