from calendar import monthcalendar
from datetime import datetime
from typing import Final, final, Literal, Optional
from zoneinfo import ZoneInfo

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.callback_data import CallbackData

from config import bot_config


@final
class CalendarBot:
    """
    Interactive calendar implementation.
    """
    __slots__ = 'lang', 'month', 'year', 'names_on_calendar'

    callback = CallbackData('calendar_main', 'select', 'year', 'month', 'day')
    ignore_callback = callback.new("IGNORE", -1, -1, -1)

    def __init__(self, tz: str = bot_config.time_zone, lang: Literal['ru', 'en'] = 'ru') -> None:
        self.lang: str = lang
        self.month: int = datetime.now(tz=ZoneInfo(tz)).month
        self.year: int = datetime.now(tz=ZoneInfo(tz)).year
        self.names_on_calendar: dict = self._define_a_collection_of_names()

    def _define_a_collection_of_names(self) -> dict:
        """
        Language set selection.
        :return: names of months and days in dict
        """
        MONTHS_EN: Final[tuple] = (
            'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        )
        MONTHS_RU: Final[tuple] = (
            'Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'
        )
        DAYS_EN: Final[tuple] = 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'
        DAYS_RU: Final[tuple] = 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'

        if self.lang == 'ru':
            return {
                'MONTHS': MONTHS_RU,
                'DAYS': DAYS_RU,
            }
        else:
            return {
                'MONTHS': MONTHS_EN,
                'DAYS': DAYS_EN,
            }

    def enable(self, year: Optional[int] = None) -> InlineKeyboardMarkup:
        """
        Shows the years.
        :param year: this year
        :return: keyboard
        """
        if not year:
            year: int = self.year
        inline_kb = InlineKeyboardMarkup(row_width=3)
        inline_kb.row()
        for value in range(year - 4, year + 2):
            inline_kb.insert(
                InlineKeyboardButton(
                    value if value != self.year else '📍',
                    callback_data=self.callback.new("SET-YEAR", value, -1, -1)
                )
            )
        inline_kb.row()
        inline_kb.add(
            InlineKeyboardButton('🔙', callback_data=self.callback.new("PREV-YEARS", year, -1, -1)),
            InlineKeyboardButton('🔜', callback_data=self.callback.new("NEXT-YEARS", year, -1, -1)),
        )
        return inline_kb

    def _get_month_kb(self, year: int | str) -> InlineKeyboardMarkup:
        """
        Shows the months.
        :param year: selected year
        :return: keyboard
        """
        inline_kb = InlineKeyboardMarkup(row_width=6)
        inline_kb.row()
        inline_kb.add(
            InlineKeyboardButton(" ", callback_data=self.ignore_callback),
            InlineKeyboardButton(str(year), callback_data=self.callback.new("START", year, -1, -1)),
            InlineKeyboardButton(" ", callback_data=self.ignore_callback),
        )
        inline_kb.row()
        self._button_month(slice_index=slice(0, 6), year=year, keyboard=inline_kb)
        inline_kb.row()
        self._button_month(slice_index=slice(6, 12), year=year, keyboard=inline_kb)
        return inline_kb

    def _button_month(self, slice_index, year, keyboard) -> None:
        for month in self.names_on_calendar['MONTHS'][slice_index]:
            keyboard.insert(InlineKeyboardButton(
                month if year != self.year or month != self.names_on_calendar['MONTHS'][self.month - 1] else '📍',
                callback_data=self.callback.new(
                    "SET-MONTH", year, self.names_on_calendar['MONTHS'].index(month) + 1, -1
                )
            ))

    def _get_days_kb(self, year: int, month: int) -> InlineKeyboardMarkup:
        """
        Shows the days.
        :param year: selected year
        :param month: selected month
        :return: keyboard
        """
        inline_kb = InlineKeyboardMarkup(row_width=7)
        inline_kb.row()
        inline_kb.add(
            InlineKeyboardButton(
                str(year), callback_data=self.callback.new("START", year, -1, -1)
            ),
            InlineKeyboardButton(
                self.names_on_calendar['MONTHS'][month - 1],
                callback_data=self.callback.new("SET-YEAR", year, -1, -1)
            )
        )
        inline_kb.row()
        for day in self.names_on_calendar['DAYS']:
            inline_kb.insert(InlineKeyboardButton(day, callback_data=self.ignore_callback))

        for week in monthcalendar(year, month):
            inline_kb.row()
            for day in week:
                if day == 0:
                    inline_kb.insert(InlineKeyboardButton(' ', callback_data=self.ignore_callback))
                    continue
                inline_kb.insert(InlineKeyboardButton(
                    str(day), callback_data=self.callback.new('SET-DAY', year, month, day)
                ))
        return inline_kb

    async def process_selection(self, query: CallbackQuery, data: dict) -> tuple:
        """
        Generates and returns the selected date.
        """
        return_data: tuple = False, None
        for item in ('year', 'month', 'day'):
            if isinstance(data.get(item), str):
                data[item]: int = int(data[item])

        match data.get('select'):
            case 'IGNORE':
                await query.answer(cache_time=60)
            case 'SET-YEAR':
                await query.message.edit_reply_markup(self._get_month_kb(data['year']))
            case 'PREV-YEARS':
                new_year: int = data['year'] - 5
                await query.message.edit_reply_markup(self.enable(new_year))
            case 'NEXT-YEARS':
                new_year: int = data['year'] + 5
                await query.message.edit_reply_markup(self.enable(new_year))
            case 'START':
                await query.message.edit_reply_markup(self.enable(data['year']))
            case 'SET-MONTH':
                await query.message.edit_reply_markup(self._get_days_kb(data['year'], data['month']))
            case 'SET-DAY':
                await query.message.delete_reply_markup()
                return_data: tuple = True, datetime(data['year'], data['month'], data['day']).date()
        return return_data


calendar_bot_ru = CalendarBot()
calendar_bot_en = CalendarBot(lang='en')
