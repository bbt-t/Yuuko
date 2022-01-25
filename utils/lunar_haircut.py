from bs4 import BeautifulSoup
from aiohttp import ClientSession
from aioredis import from_url as aioredis_from_url

from config import time_zone, redis_data_cache, work_with_api
from loader import logger_guru, get_time_now




async def lunar_calendar_haircut() -> str:
    """
    Forms a list of "favorable" days.
    """
    time = get_time_now(time_zone)
    year, month = time.strftime('%Y'), time.strftime('%B').lower()

    async with aioredis_from_url(**redis_data_cache) as connect_redis:

        if data := await connect_redis.get('haircut'):
            text: str = data.decode()
        else:
            async with ClientSession() as session:
                async with session.get('{}{}/{}'.format(work_with_api['OTHER']['HAIRCUT_PARSE'], year, month)) as resp:

                    if resp.status != 200:
                        logger_guru.warning(f"{resp.status=} : Bad request!")
                        return 'Что-то пошло не так...попробуй позже.'

                    soup = BeautifulSoup(await resp.text(), 'lxml')

            items = soup.find_all(class_='next_phase month_row green2')

            text: str = ','.join(
                sorted(
                    {data.text.split()[0] for data in items if data.find('span', style='font-weight: bold;')}, key=int
                )
            )
            await connect_redis.set('haircut', text)
    return text
