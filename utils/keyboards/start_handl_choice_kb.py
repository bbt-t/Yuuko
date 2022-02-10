from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


choice_of_assistant_kb_ru = InlineKeyboardMarkup()
choice_of_assistant_kb_ru.add(
    InlineKeyboardButton(text='Neko (кот)', callback_data='neko'),
    InlineKeyboardButton(text='Тян', callback_data='chan'),
    InlineKeyboardButton(text='оставить облачко', callback_data='cloud'),
)

choice_of_assistant_kb_en = InlineKeyboardMarkup()
choice_of_assistant_kb_en.add(
    InlineKeyboardButton(text='Neko (cat)', callback_data='neko'),
    InlineKeyboardButton(text='Chan', callback_data='chan'),
    InlineKeyboardButton(text='choose a cloud', callback_data='cloud'),
)

initial_setup_choice_kb_ru = InlineKeyboardMarkup()
initial_setup_choice_kb_ru.add(
    InlineKeyboardButton(text='ДАВАЙ!', callback_data='set_birthday'),
    InlineKeyboardButton(text='не, может позже...', callback_data='cancel')
)

initial_setup_choice_kb_en = InlineKeyboardMarkup()
initial_setup_choice_kb_en.add(
    InlineKeyboardButton(text="LET'S!", callback_data='set_birthday'),
    InlineKeyboardButton(text='no, maybe later...', callback_data='cancel')
)
