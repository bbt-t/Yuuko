from dataclasses import dataclass
from os import getenv
from pathlib import Path
from zoneinfo import available_timezones

from dotenv import load_dotenv


load_dotenv(verbose=True)


@dataclass(frozen=True, eq=False)
class Administrators:
    """
    Administrators:
        name - telegram id
    """
    creator: str


@dataclass(frozen=True, eq=False)
class MainRedis:
    """
    Base settings Redis.
    """
    port: int | str
    password: str
    prefix: str
    host: str = 'localhost'

    def as_dict(self):
        return {
            'host': self.host,
            'port': self.port,
            'password': self.password,
            'prefix': self.prefix,
        }


@dataclass(frozen=True, eq=False)
class CacheRedis:
    """
    Redis settings for cache.
    """
    db: int
    password: str
    url: str = f"redis://{MainRedis.host}"

    def as_dict(self):
        return {
            'url': self.url,
            'db': self.db,
            'password': self.password,
        }


@dataclass(frozen=True, eq=False)
class ConfigRedis:
    """
    All Redis settings.
    """
    redis_for_bot: MainRedis
    redis_data_cache: CacheRedis


@dataclass(frozen=True, eq=False)
class WebHook:
    host: str
    port: int
    webhook_path: str = Path(__file__).parent

    def as_dict(self):
        return {
            'webhook_path': self.webhook_path,
            'host': self.host,
            'port': self.port,
        }

    def __post_init__(self):
        if not isinstance(self.port, int):
            raise TypeError('type PORT must be integer!')


@dataclass(frozen=True, eq=False)
class ConfigHook:
    """
    Settings for start bot (webhook).
    """
    WEBHOOK: WebHook
    WEBHOOK_URL: str


@dataclass(frozen=True, eq=False)
class YandexAPI:
    """
    Yandex API info.
    """
    FOLDER_ID: str
    API_YA_STT: str
    API_YA_TTS: str


@dataclass(frozen=True, eq=False)
class OtherAPI:
    HORO_XML: str
    HORO_EN: str
    HAIRCUT_PARSE: str
    OCR_URL: str | None


@dataclass(frozen=True, eq=False)
class WeatherAPI:
    """
    Weather API's info.
    """
    API_WEATHER: str
    API_WEATHER2: str
    CITY_WEATHER: str


@dataclass(frozen=True, eq=False)
class ConfigAPI:
    yandex: YandexAPI
    weather: WeatherAPI
    other: OtherAPI


@dataclass(frozen=True, eq=False, slots=True)
class ConfigBot:
    BOT_TOKEN: str
    bot_administrators: Administrators
    redis: ConfigRedis
    hook_info: ConfigHook
    work_with_api: ConfigAPI
    DB_NAME: str = 'database'
    time_zone: str = 'UTC'

    def __post_init__(self):
        if self.time_zone not in available_timezones():
            raise ValueError(
                'You can choose only available timezones!\n'
                'more info > https://docs.python.org/3/library/zoneinfo.html#zoneinfo.available_timezones'
            )


def create_config() -> ConfigBot:
    """
    Create config.
    :return: ConfigBot object
    """
    return ConfigBot(
        time_zone=getenv('TIMEZONE'),
        BOT_TOKEN=getenv('BOT_TOKEN'),
        DB_NAME=getenv('DB_NAME'),
        bot_administrators=Administrators(creator=getenv('CREATOR')),
        redis=ConfigRedis(
            redis_for_bot=MainRedis(
                host=getenv('HOST_REDIS'),
                port=getenv('PORT_REDIS'),
                password=getenv('PASS_REDIS'),
                prefix='fsm_key',
            ),
            redis_data_cache=CacheRedis(
                url=f"redis://{getenv('HOST_REDIS')}",
                db=1,
                password=getenv('PASS_REDIS'),
            )
        ),
        hook_info=ConfigHook(
            WEBHOOK=WebHook(
                webhook_path=getenv('WEBHOOK_PATH'),
                host=getenv('WEBAPP_HOST'),
                port=3001,
            ),
            WEBHOOK_URL=f"{getenv('WEBHOOK_HOST')}{getenv('WEBHOOK_PATH')}"
        ),
        work_with_api=ConfigAPI(
            yandex=YandexAPI(
                FOLDER_ID=getenv('FOLDER_ID'),
                API_YA_STT=getenv('API_YA_STT'),
                API_YA_TTS=getenv('API_YA_TTS')
            ),
            weather=WeatherAPI(
                API_WEATHER=getenv('API_WEATHER'),
                API_WEATHER2=getenv('API_WEATHER2'),
                CITY_WEATHER=getenv('CITY_WEATHER'),
            ),
            other=OtherAPI(
                HORO_XML=getenv('HORO_XML'),
                HORO_EN=getenv('HORO_EN'),
                HAIRCUT_PARSE=getenv('HAIRCUT_PARSE'),
                OCR_URL=getenv('OCR_URL'),
            ),
        )
    )


bot_config: ConfigBot = create_config()
