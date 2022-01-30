from ipaddress import IPv4Address
from typing import Literal

from pydantic import BaseModel, HttpUrl, AnyHttpUrl, AnyUrl, RedisDsn, StrictInt, StrictStr


class RedisConfBot(BaseModel):
    host: IPv4Address | Literal['localhost']
    port: int
    password: StrictStr | None
    prefix: StrictStr | None


class RedisConfDataCache(BaseModel):
    url: RedisDsn
    password: StrictStr | None
    db: StrictInt


class _Webhook(BaseModel):
    webhook_path: StrictStr
    host: IPv4Address
    port: StrictInt


class WebHook(BaseModel):
    WEBHOOK: _Webhook
    WEBHOOK_URL: HttpUrl


class _Yandex(BaseModel):
    FOLDER_ID: StrictStr
    API_YA_STT: StrictStr
    API_YA_TTS: StrictStr


class _Weather(BaseModel):
    API_WEATHER: StrictStr
    API_WEATHER2: StrictStr
    CITY_WEATHER: StrictStr


class _Other(BaseModel):
    HORO_XML: HttpUrl
    HORO_EN: HttpUrl
    HAIRCUT_PARSE: AnyHttpUrl
    OCR_URL: AnyUrl | None


class WorkApiAll(BaseModel):
    YANDEX: _Yandex
    WEATHER: _Weather
    OTHER: _Other | None



