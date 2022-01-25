from enum import Enum, unique

from config import work_with_api


@unique
class SendStickers(Enum):
    welcome = 'CAACAgIAAxkBAAEDZZZhp4UKWID3NNoRRLywpZPBSmpGUwACVwEAAhAabSKlKzxU-3o0qiIE'
    you_were_bad = 'CAACAgIAAxkBAAEDZZhhp4W7R60LkP0BQaSR3B-agVBpswACpAEAAhAabSIYtWa5P_cfjSIE'
    seeking = 'CAACAgIAAxkBAAEDZZphp4c3RNVqorg6zd0JRBzjB29bXwACcAEAAhAabSIN3A9bRLCgiyIE'
    ok = 'CAACAgQAAxkBAAEDZZ9hp4p16Vjuw2lxS_1gb6riIzkeaQACAwADo4VmBNnyQ162xzvhIgQ'
    i_do_not_understand = 'CAACAgIAAxkBAAEDZaFhp4qDluGGvnCQe2WhofQ3r2wtfgACrAEAAhAabSJ41lvmGuTmxyIE'
    sad_ok = 'CAACAgIAAxkBAAEDZaNhp4w03jKO6vfOzbiZ7E13RAwaZwACYQEAAhAabSLviIx9qppNByIE'
    yippee = 'CAACAgQAAxkBAAEDZb9hp54mKnGg17yOn8hhgC_neGmFsAACPgEAAqghIQaycvGBPmKyDCIE'
    yipee_2_girls = 'CAACAgIAAxkBAAEDZdthp74uT7HCmBSru9Ehma95SpVSIQACZQEAAhAabSJhjGLAZuk2oSIE'
    hmm = 'CAACAgIAAxkBAAEDZnphqNiE9Hq7mRGha9j-nJfYGOSPgAACeg0AAsCf8Ev-fdx9cnSwwSIE'
    fear = 'CAACAgIAAxkBAAEDbxphr6Avra8WTksfENEkK1GuHIpwpQACZAEAAhAabSJJXz3XqubCyiME'
    great = 'CAACAgIAAxkBAAEDq65h3qyS-PLtDPPMqsVTJqzk5fiNVQACWQEAAhAabSIdlWw5X85AHyME'
    order_accepted = 'CAACAgIAAxkBAAEDq7Bh3q377Dt2SZfuysrGb-QDkNgf3AACagEAAhAabSLoW9qOycF19iME'
    something_is_wrong = 'CAACAgIAAxkBAAEDq7Jh3q39AYPYM8HiYb9PEsH6ja0dYAACYgEAAhAabSLNwhNkGRe1tyME'
    love_you = 'CAACAgIAAxkBAAEDrIdh3yzY_T_l_z6lYv0DPtnjyYyB8wACkgEAAhAabSLrhFu8iLyTaSME'


@unique
class ApiInfo(Enum):
    WEATHER_API_BASIC = f"https://api.openweathermap.org/data/2.5/weather?q={work_with_api['WEATHER']['CITY_WEATHER']}&appid={work_with_api['WEATHER']['API_WEATHER']}&units=metric&lang=ru"
    WEATHER_API_RESERVE = f"http://dataservice.accuweather.com/forecasts/v1/daily/1day/CITY?apikey={work_with_api['WEATHER']['API_WEATHER2']}&language=ru-ru&metric=true&details=true"
    GET_CITY_ID = f"http://dataservice.accuweather.com/locations/v1/cities/autocomplete?apikey={work_with_api['WEATHER']['API_WEATHER2']}&q={work_with_api['WEATHER']['CITY_WEATHER']}"
    STT_YANDEX = "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize"
    TTS_YANDEX = "https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize"
