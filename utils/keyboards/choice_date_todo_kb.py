from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton



choice = InlineKeyboardMarkup(row_width=1,
                              inline_keyboard=[
                                  [
                                      InlineKeyboardButton(
                                          text='на сегодня',
                                          callback_data='today'
                                      ),
                                      InlineKeyboardButton(
                                          text='на завтра',
                                          callback_data='tomorrow'
                                      ),
                                      InlineKeyboardButton(
                                          text='отмена',
                                          callback_data='cancel'
                                          )
                                  ],

                              ])

start_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
start_kb.row('Bыбрать дату')