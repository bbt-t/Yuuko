from bs4 import BeautifulSoup
from requests import get as request_get

from config import HAIRCUT_PARSE, time_now
from loader import logger_guru




async def lunar_calendar_haircut():

    year, month = time_now.strftime('%Y'), time_now.strftime('%B').lower()
    req = request_get('{}{}/{}'.format(HAIRCUT_PARSE, year, month))

    if req.status_code != 200:
        logger_guru.warning(f"{req.status_code=} : Bad request!")
        return 'Что-то пошло не так...попробуй позже.'

    soup = BeautifulSoup(req.text, 'html.parser')
    items = soup.find_all(class_='next_phase month_row green2')

    text: str = '\n'.join(sorted(
        {' '.join(data.text.split()[:2]) for data in items if data.find('span', style='font-weight: bold;')},
        key=lambda x: int(x[:2])
    ))
    return text
