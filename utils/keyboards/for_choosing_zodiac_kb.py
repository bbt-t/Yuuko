from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


choice_zodiac_keyboard = InlineKeyboardMarkup(row_width=2)
choice_zodiac_keyboard.add(
    InlineKeyboardButton(text='Овен 21 марта – 20 апреля', callback_data='aries'),
    InlineKeyboardButton(text='Телец 21 апреля – 20 мая', callback_data='taurus'),
    InlineKeyboardButton(text='Близнецы 21 мая – 21 июня', callback_data='gemini'),
    InlineKeyboardButton(text='Рак 22 июня – 22 июля', callback_data='cancer'),
    InlineKeyboardButton(text='Лев 23 июля – 23 августа', callback_data='leo'),
    InlineKeyboardButton(text='Дева 24 августа – 23 сентября', callback_data='virgo'),
    InlineKeyboardButton(text='Весы 24 сентября – 23 октября', callback_data='libra'),
    InlineKeyboardButton(text='Скорпион 24 октября – 22 ноября', callback_data='scorpio'),
    InlineKeyboardButton(text='Стрелец 23 ноября – 21 декабря', callback_data='sagittarius'),
    InlineKeyboardButton(text='Козерог 22 декабря – 20 января', callback_data='capricorn'),
    InlineKeyboardButton(text='Водолей 21 января – 20 февраля', callback_data='aquarius'),
    InlineKeyboardButton(text='Рыбы 21 февраля – 20 марта', callback_data='pisces')
)

choice_day_zodiac_keyboard = InlineKeyboardMarkup(row_width=2)
choice_day_zodiac_keyboard.add(
    InlineKeyboardButton(text='на сегодня', callback_data='today'),
    InlineKeyboardButton(text='на завтра', callback_data='tomorrow')
)