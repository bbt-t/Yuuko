from enum import Enum
from pickle import loads as pickle_loads

from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import Update, Delete

from loader import Base, engine
from .sql_table import OtherInfo, Users


async def start_db() -> None:
    """
    Drop and Create table
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def add_user(telegram_id: int, lang: str = 'ru') -> None:
    """
    Add user in table 'Users'
    :param telegram_id: telegram id
    :param lang: device language
    """
    if lang is None:
        lang = 'ru'
    user = Users(telegram_id=telegram_id, selected_bot_lang=lang)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        async with session.begin():
            session.add(user)
        await session.commit()
    await engine.dispose()


async def add_other_info(telegram_id: int, name: str, info_for_save: bytes) -> None:
    """
    Adds an encrypted password in table 'Others_info'
    :param telegram_id: telegram user id
    :param name: password name
    :param info_for_save: password
    """
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        async with session.begin():
            session.add(OtherInfo(telegram_id=telegram_id, name_pass=name, pass_item=info_for_save))
        await session.commit()
    await engine.dispose()


async def update_pass(telegram_id: int, name_pass: str, info_for_save: bytes) -> None:
    """
    Sets a new password for verification
    :param telegram_id: telegram user id
    :param name_pass: password name to change
    :param info_for_save: password
    """
    sql = Update(OtherInfo).where(OtherInfo.telegram_id == telegram_id, OtherInfo.name_pass == name_pass).values(
        pass_item=info_for_save
    )
    async with AsyncSession(engine) as session:
        await session.execute(sql)
        await session.commit()
    await engine.dispose()


async def update_personal_pass(telegram_id: int | str, personal_pass: str | None) -> None:
    """
    Sets a new codeword for verification.
    :param telegram_id: telegram user id
    :param personal_pass: password
    """
    sql = Update(Users).where(Users.telegram_id == telegram_id).values(personal_pass=personal_pass)
    async with AsyncSession(engine) as session:
        await session.execute(sql)
        await session.commit()
    await engine.dispose()


async def update_birthday(telegram_id: int | str, birthday) -> None:
    """
    Sets the values of the user's birthday.
    :param telegram_id: telegram user id
    :param birthday: birthday date
    """
    sql = Update(Users).where(Users.telegram_id == telegram_id).values(birthday=birthday)
    async with AsyncSession(engine) as session:
        await session.execute(sql)
        await session.commit()
    await engine.dispose()


async def update_bot_language(telegram_id: int | str, lang: str) -> None:
    """
    Changes the language of the bot.
    :param telegram_id: telegram user id
    :param lang: language
    """
    sql = Update(Users).where(Users.telegram_id == telegram_id).values(selected_bot_lang=lang)
    async with AsyncSession(engine) as session:
        await session.execute(sql)
        await session.commit()
    await engine.dispose()


async def update_bot_skin(telegram_id: int | str, skin: str) -> None:
    """
    Changes the skin of the bot.
    :param telegram_id: telegram user id
    :param skin: user-selected skin
    """
    sql = Update(Users).where(Users.telegram_id == telegram_id).values(selected_bot_skin=skin)
    async with AsyncSession(engine) as session:
        await session.execute(sql)
        await session.commit()
    await engine.dispose()


async def check_personal_pass(telegram_id: int | str) -> str:
    """
    To check the entered codeword.
    :param telegram_id: telegram user id
    :return: password for verification
    """
    async with engine.connect() as conn:
        result = await conn.execute(select(Users.personal_pass).where(Users.telegram_id == telegram_id))
    await engine.dispose()
    return result.scalar_one()


async def select_pass(telegram_id: int | str, name: str) -> str:
    """
    Gets password and extracts from pkl.
    :param telegram_id: telegram user id
    :param name: saved password name
    :return: password
    """
    async with engine.connect() as conn:
        result = await conn.execute(select(OtherInfo.pass_item).where(
            OtherInfo.telegram_id == telegram_id,
            OtherInfo.name_pass == name
        ))
    await engine.dispose()
    return pickle_loads(result.scalar_one())


async def select_user(telegram_id: int | str) -> tuple:
    """
    Selects a user by his ID.
    :param telegram_id: telegram user id
    :return: user info
    """
    async with engine.connect() as conn:
        result = await conn.execute(select(Users).where(Users.telegram_id == telegram_id))
    await engine.dispose()
    return result.fetchone()


async def select_all_users() -> list:
    """
    Selects all users telegram id.
    :return: all telegram id in list
    """
    async with engine.connect() as conn:
        result = await conn.execute(select(Users.telegram_id))
    await engine.dispose()
    return result.scalars().all()


async def select_user_birthday(telegram_id: int | str) -> str:
    """
    Selects a user's birthday by their telegram id.
    :param telegram_id: telegram user id
    :return: user info
    """
    async with engine.connect() as conn:
        result = await conn.execute(select(Users.birthday).where(Users.telegram_id == telegram_id))
    await engine.dispose()
    return result.scalar_one()


async def select_skin(telegram_id: int | str):
    """
    Selects the selected bot-skin by user telegram id.
    :param telegram_id: telegram user id
    :return: user info in enum
    """
    async with engine.connect() as conn:
        result = await conn.execute(select(Users.selected_bot_skin).where(Users.telegram_id == telegram_id))
    await engine.dispose()
    return result.scalar_one().value


async def select_bot_language(telegram_id: int | str) -> str:
    """
    Selects the selected language by user telegram id.
    :param telegram_id: telegram user id
    :return: user info in enum
    """
    async with engine.connect() as conn:
        result = await conn.execute(select(Users.selected_bot_lang).where(Users.telegram_id == telegram_id))
    await engine.dispose()
    return result.scalar_one()


async def select_lang_and_skin(telegram_id: int | str) -> tuple[str, Enum]:
    """
    Select language and skin
    """
    async with engine.connect() as conn:
        result = await conn.execute(
            select(Users.selected_bot_lang, Users.selected_bot_skin).where(Users.telegram_id == telegram_id)
        )
    await engine.dispose()
    lang, skin = result.one()

    return lang, skin.value


async def check_valid_user(telegram_id: int) -> bool:
    """
    Сhecks the user by his telegram id.
    :param telegram_id: telegram user id
    :return: True or False
    """
    async with engine.connect() as conn:
        result = await conn.execute(select(Users.created_time).where(Users.telegram_id == telegram_id))
    await engine.dispose()
    return not result.one_or_none()


async def delete_user(telegram_id: int | str) -> None:
    """
    Delete a user by his ID.
    :param telegram_id: telegram user id
    :return: user info
    """
    sql = Delete(Users).where(Users.telegram_id == telegram_id)
    async with AsyncSession(engine) as session:
        await session.execute(sql)
        await session.commit()
    await engine.dispose()
