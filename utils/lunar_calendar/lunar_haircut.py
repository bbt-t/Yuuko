from bs4 import BeautifulSoup

from httpx import AsyncClient

from config import HAIRCUT_PARSE, time_now
from loader import logger_guru




async def lunar_calendar_haircut() -> str:
    """
    Forms a list of "favorable" days.
    """
    year, month = time_now.strftime('%Y'), time_now.strftime('%B').lower()

    async with AsyncClient() as request:
        req = await request.get('{}{}/{}'.format(HAIRCUT_PARSE, year, month))

    if req.status_code != 200:
        logger_guru.warning(f"{req.status_code=} : Bad request!")
        return 'Что-то пошло не так...попробуй позже.'

    soup = BeautifulSoup(req.text, 'html.parser')
    items = soup.find_all(class_='next_phase month_row green2')

    text: str = ','.join(
        sorted({data.text.split()[0] for data in items if data.find('span', style='font-weight: bold;')}, key=int)
    )
    return text
