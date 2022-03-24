from enum import Enum, unique

from config import bot_config


@unique
class CloudStickers(Enum):
    welcome = 'CAACAgIAAxkBAAEDy9dh-5AckZRcKWOsNguanJZwCi6uCAACXEAAAulVBRh-S-guvy5fdSME'
    you_were_bad = 'CAACAgIAAxkBAAEDy91h-5BEoyslhc2ZUIpeyoZ9EcIZmwACV0AAAulVBRiYDqQhsas8lyME'
    seeking = 'CAACAgIAAxkBAAEDzFdh-8b5C577JtUf9Tak_ctpnJsnjQACfkAAAulVBRgl4oApyAxAziME'
    i_do_not_understand = 'CAACAgIAAxkBAAEDy-Fh-5BaBxU1HUnlBULq3ECQ_a3D0gACbkAAAulVBRgSBY5GoL23USME'
    sad_ok = 'CAACAgIAAxkBAAEDy-Vh-5CYqmlQ_iszmdmQ395ShiX3XAACVkAAAulVBRhtBVW9V0EkhSME'
    fear = 'CAACAgIAAxkBAAEDzF1h-8fI-GL1rTH5AAFj-YP-ATfUz84AAlRAAALpVQUYOShbPvaxUtEjBA'
    great = 'CAACAgIAAxkBAAEDzFlh-8d6G-aNjSKBwQjUkVAnnrJC6QACbEAAAulVBRjQ4maqhDe1rCME'
    order_accepted = 'CAACAgIAAxkBAAEDzgxh_S_BSCXy8xBLIiJ-euS862ONPgACYkAAAulVBRgswaMrAtM9jyME'
    something_is_wrong = 'CAACAgIAAxkBAAEDzF9h-8gzug-5JOsM9nPV4aomPmEnFAACf0AAAulVBRh1wD51yaAZMCME'
    love_you = 'CAACAgIAAxkBAAEDy_dh-5INl4hc-MUPjxLf5DtrXqFhZAACWEAAAulVBRhX7ZJ5mjvjViME'


@unique
class ChanStickers(Enum):
    welcome = 'CAACAgIAAxkBAAEDZZZhp4UKWID3NNoRRLywpZPBSmpGUwACVwEAAhAabSKlKzxU-3o0qiIE'
    you_were_bad = 'CAACAgIAAxkBAAEDZZhhp4W7R60LkP0BQaSR3B-agVBpswACpAEAAhAabSIYtWa5P_cfjSIE'
    seeking = 'CAACAgIAAxkBAAEDZZphp4c3RNVqorg6zd0JRBzjB29bXwACcAEAAhAabSIN3A9bRLCgiyIE'
    i_do_not_understand = 'CAACAgIAAxkBAAEDZaFhp4qDluGGvnCQe2WhofQ3r2wtfgACrAEAAhAabSJ41lvmGuTmxyIE'
    sad_ok = 'CAACAgIAAxkBAAEDZaNhp4w03jKO6vfOzbiZ7E13RAwaZwACYQEAAhAabSLviIx9qppNByIE'
    fear = 'CAACAgIAAxkBAAEDbxphr6Avra8WTksfENEkK1GuHIpwpQACZAEAAhAabSJJXz3XqubCyiME'
    great = 'CAACAgIAAxkBAAEDq65h3qyS-PLtDPPMqsVTJqzk5fiNVQACWQEAAhAabSIdlWw5X85AHyME'
    order_accepted = 'CAACAgIAAxkBAAEDq7Bh3q377Dt2SZfuysrGb-QDkNgf3AACagEAAhAabSLoW9qOycF19iME'
    something_is_wrong = 'CAACAgIAAxkBAAEDq7Jh3q39AYPYM8HiYb9PEsH6ja0dYAACYgEAAhAabSLNwhNkGRe1tyME'
    love_you = 'CAACAgIAAxkBAAEDrIdh3yzY_T_l_z6lYv0DPtnjyYyB8wACkgEAAhAabSLrhFu8iLyTaSME'


@unique
class NekoStickers(Enum):
    welcome = 'CAACAgIAAxkBAAEDzfZh_SxkHF9HWPYT7QsGIdbl0HIhJwAC6BAAAsFHYErUYdMPqGKuxiME'
    you_were_bad = 'CAACAgIAAxkBAAEDzgJh_S0v_1xlZnlEMRzY53QNSK5LoQACxRIAAj2xWUql_s73PSpRjyME'
    seeking = 'CAACAgIAAxkBAAEDzghh_S8E9L-45XSZN8mvGY_PwGhccwACehMAAuZBYEq-qUSmuPPI-iME'
    i_do_not_understand = 'CAACAgIAAxkBAAEDzfxh_SyJPuQGrtlUfQ2F7OpoK6lZWgACzBcAAiysYUqPB5V_BH6XkCME'
    sad_ok = 'CAACAgIAAxkBAAEDzgABYf0srLvSunGTF7p04doWzzQi_dIAAhIVAAJmK1lKC1rpwGlleq4jBA'
    fear = 'CAACAgIAAxkBAAEDzgZh_S7h19czfQABtvnipSUZoUkHSpkAAugRAAL8nVlKx27aOwMk44gjBA'
    great = 'CAACAgIAAxkBAAEDzfph_Sx0IdfHM7FMT4t7goqLh0Lv3wAC-xEAAmvkWEoKPj6s6cyDoSME'
    order_accepted = 'CAACAgIAAxkBAAEDzgph_S-CpxkD5pvMg5SDBWqs5YUQJgADEQACh9BYSpOe9dWAw06ZIwQ'
    something_is_wrong = 'CAACAgIAAxkBAAEDzfhh_SxpWuQ4p_qBmUea85LCYeHfWgACNBIAAtHDWEoarkwf4Q8DliME'
    love_you = 'CAACAgIAAxkBAAEDzgRh_S2DlowAAZeiKfxIFFuVeaXAF3AAAtUWAAIMDVlKW0S49fa0CKEjBA'


class BotSkins(Enum):
    cloud = CloudStickers
    chan = ChanStickers
    neko = NekoStickers


@unique
class ApiInfo(Enum):
    WEATHER_API_BASIC = (
        f"https://api.openweathermap.org/data/2.5/"
        f"weather?q={bot_config.work_with_api.weather.CITY_WEATHER}&"
        f"appid={bot_config.work_with_api.weather.API_WEATHER}&units=metric&lang=ru"
    )
    WEATHER_API_RESERVE = (
        f"http://dataservice.accuweather.com/forecasts/v1/daily/1day/CITY?"
        f"apikey={bot_config.work_with_api.weather.API_WEATHER2}&language=ru-ru&metric=true&details=true"
    )
    GET_CITY_ID = (
        f"http://dataservice.accuweather.com/locations/v1/cities/autocomplete?"
        f"apikey={bot_config.work_with_api.weather.API_WEATHER2}&q={bot_config.work_with_api.weather.CITY_WEATHER}"
    )
    STT_YANDEX = "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize"
    TTS_YANDEX = "https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize"
