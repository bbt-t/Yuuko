import pytest
from zoneinfo import available_timezones

import config
from tests.schemas.pydantic_schemas import RedisConfBot, RedisConfDataCache, WebHook, WorkApiAll


@pytest.mark.parametrize('token', [config.BOT_TOKEN])
def test_bot_token(token):
    assert isinstance(token, str)
    assert len(token) == 46


def test_timezone():
    assert isinstance(config.time_zone, str)
    assert config.time_zone in available_timezones()


def test_db_name_type():
    assert isinstance(config.DB_NAME, str)


def test_redis_for_bot_type():
    assert RedisConfBot.parse_obj(config.redis_for_bot)


def test_redis_data_cache_type():
    assert RedisConfDataCache.parse_obj(config.redis_data_cache)


def test_webhook_type():
    assert WebHook.parse_obj(config.hook_info)


def test_work_api_type():
    assert WorkApiAll.parse_obj(config.work_with_api)
