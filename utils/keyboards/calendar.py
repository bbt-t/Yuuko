from calendar import monthcalendar
from datetime import datetime
from typing import Final, final

from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


calendar_cb = CallbackData('dialog_calendar', 'run', 'year', 'month', 'day')
ignore_callback = calendar_cb.new("IGNORE", -1, -1, -1)


@final
class CalendarBot:
    """
    Interactive calendar implementation.
    """
    __slots__ = 'lang', 'month', 'year'

    MONTHS_EN: Final[tuple] = (
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    )
    MONTHS_RU: Final[tuple] = (
        'Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'
    )
    DAYS_EN: Final[tuple] = 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'
    DAYS_RU: Final[tuple] = 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'

    def __init__(self, year: int = datetime.now().year, month: int = datetime.now().month, lang: str = 'ru'):
        self.lang = lang
        self.month = month
        self.year = year

    async def enable(self, year: int = datetime.now().year) -> InlineKeyboardMarkup:
        """
        Shows the years.
        :param year: this year
        :return: keyboard
        """
        inline_kb = InlineKeyboardMarkup(row_width=3)
        inline_kb.row()
        for value in range(year - 4, year + 2):
            if value == datetime.now().year:
                 value = f'▶ {value} ◀'

            inline_kb.insert(
                InlineKeyboardButton(value, callback_data=calendar_cb.new("SET-YEAR", value, -1, -1))
            )
        inline_kb.row()
        inline_kb.add(
            InlineKeyboardButton('🔙', callback_data=calendar_cb.new("PREV-YEARS", year, -1, -1)),
            InlineKeyboardButton('🔜', callback_data=calendar_cb.new("NEXT-YEARS", year, -1, -1)),
        )
        return inline_kb

    async def get_month_kb(self, year: int | str) -> InlineKeyboardMarkup:
        """
        Shows the months.
        :param year: selected year
        :return: keyboard
        """
        if isinstance(year, str):
            year: int = int(''.join(filter(str.isnumeric, year)))
        inline_kb = InlineKeyboardMarkup(row_width=6)
        inline_kb.row()
        inline_kb.add(
            InlineKeyboardButton(" ", callback_data=ignore_callback),
            InlineKeyboardButton(year, callback_data=calendar_cb.new("START", year, -1, -1)),
            InlineKeyboardButton(" ", callback_data=ignore_callback),
        )
        inline_kb.row()
        if self.lang == 'ru':
            for month in self.MONTHS_RU[0:6]:
                inline_kb.insert(
                    InlineKeyboardButton(
                        month,
                        callback_data=calendar_cb.new(
                            "SET-MONTH", year, self.MONTHS_RU.index(month) + 1, -1
                        )
                    )
                )
            inline_kb.row()
            for month in self.MONTHS_RU[6:12]:
                inline_kb.insert(
                    InlineKeyboardButton(
                        month,
                        callback_data=calendar_cb.new(
                            "SET-MONTH", year, self.MONTHS_RU.index(month) + 1, -1
                        )
                    )
                )
        else:
            for month in self.MONTHS_EN[0:6]:
                inline_kb.insert(
                    InlineKeyboardButton(
                        month,
                        callback_data=calendar_cb.new(
                            "SET-MONTH", year, self.MONTHS_EN.index(month) + 1, -1
                        )
                    )
                )
            inline_kb.row()
            for month in self.MONTHS_EN[6:12]:
                inline_kb.insert(
                    InlineKeyboardButton(
                        month,
                        callback_data=calendar_cb.new("SET-MONTH", year, self.MONTHS_EN.index(month) + 1, -1)
                    )
                )
        return inline_kb

    async def get_days_kb(self, year: int, month: int) -> InlineKeyboardMarkup:
        """
        Shows the days.
        :param year: selected year
        :param month: selected month
        :return: keyboard
        """
        if isinstance(year, str):
            year: int = int(''.join(filter(str.isnumeric, year)))

        inline_kb = InlineKeyboardMarkup(row_width=7)
        inline_kb.row()
        inline_kb.add(
            InlineKeyboardButton(
                year, callback_data=calendar_cb.new("START", year, -1, -1)
            ),
            InlineKeyboardButton(
                self.MONTHS_EN[month - 1], callback_data=calendar_cb.new("SET-YEAR", year, -1, -1)
            )
        )
        inline_kb.row()
        if self.lang == 'ru':
            for day in self.DAYS_RU:
                inline_kb.insert(InlineKeyboardButton(day, callback_data=ignore_callback))
        else:
            for day in self.DAYS_EN:
                inline_kb.insert(InlineKeyboardButton(day, callback_data=ignore_callback))

        for week in monthcalendar(year, month):
            inline_kb.row()
            for day in week:
                if day == 0:
                    inline_kb.insert(InlineKeyboardButton(' ', callback_data=ignore_callback))
                    continue
                inline_kb.insert(InlineKeyboardButton(
                    str(day), callback_data=calendar_cb.new('SET-DAY', year, month, day)
                ))
        return inline_kb

    async def process_selection(self, query: CallbackQuery, data: dict) -> tuple:
        """
        Generates and returns the selected date.
        """
        return_data: tuple = False, None
        for el in ('year', 'month', 'day'):
            if isinstance(data.get(el), str):
                data[el]: int = int(''.join(filter(str.isnumeric, data[el])))

        match data.get('run'):
            case 'IGNORE':
                await query.answer(cache_time=60)
            case 'SET-YEAR':
                await query.message.edit_reply_markup(await self.get_month_kb(int(data['year'])))
            case 'PREV-YEARS':
                new_year: int = int(data['year']) - 5
                await query.message.edit_reply_markup(await self.enable(new_year))
            case 'NEXT-YEARS':
                new_year: int = int(data['year']) + 5
                await query.message.edit_reply_markup(await self.enable(new_year))
            case 'START':
                await query.message.edit_reply_markup(await self.enable(int(data['year'])))
            case 'SET-MONTH':
                await query.message.edit_reply_markup(await self.get_days_kb(int(data['year']), int(data['month'])))
            case 'SET-DAY':
                await query.message.delete_reply_markup()
                return_data: tuple = True, datetime(int(data['year']), int(data['month']), int(data['day'])).date()
        return return_data


calendar_bot_ru = CalendarBot()
calendar_bot_en = CalendarBot(lang='en')
