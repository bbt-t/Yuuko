from bs4 import BeautifulSoup
from aiohttp import ClientSession
from aioredis import from_url as aioredis_from_url

from config import HAIRCUT_PARSE, time_now, redis_for_data
from loader import logger_guru




async def lunar_calendar_haircut() -> str:
    """
    Forms a list of "favorable" days.
    """
    year, month = time_now.strftime('%Y'), time_now.strftime('%B').lower()

    async with aioredis_from_url(**redis_for_data) as connect_redis:

        if data := await connect_redis.get('haircut'):
            text: str = data.decode()
        else:
            async with ClientSession() as session:
                async with session.get('{}{}/{}'.format(HAIRCUT_PARSE, year, month)) as resp:

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
