from pickle import loads as pickle_loads

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update

from loader import Base, engine
from utils.db_api.sql_table import OtherInfo, Users




async def start_db():
    """
    Drop and Create table
    :return:
    """
    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def add_user(id: int, name: str):
    """
    Add user in table 'Users'
    :param id: telegram id
    :param name: user name
    """
    user = Users(telegram_id=id, full_name=name)
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        async with session.begin():
            session.add(user)
        await session.commit()
    await engine.dispose()


async def add_other_info(id: int, name: str, info_for_save: bytes):
    """
    Adds an encrypted password in table 'Others_info'
    :param id: telegram id
    :param name: password name
    :param info_for_save: password
    """
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        async with session.begin():
            session.add(OtherInfo(telegram_id=id, name_pass=name, pass_items=info_for_save))
        await session.commit()
    await engine.dispose()


async def select_user(id: int) -> str:
    """
    Selects a user by his ID
    :param id: telegram id
    :return: user info
    """
    async with engine.connect() as conn:
        result = await conn.execute(select(Users).where(Users.telegram_id == id))
    await engine.dispose()
    return result.fetchone()


async def select_pass(id: int, name: str) -> str:
    """
    gets password and extracts from pkl
    :param id: telegram id
    :param name: saved password name
    :return: password
    """
    async with engine.connect() as conn:
        result = await conn.execute(select(OtherInfo.pass_items).where(OtherInfo.telegram_id == id,
                                                                    OtherInfo.name_pass == name))
    await engine.dispose()
    return pickle_loads(result.fetchone()[0])


async def check_personal_pass(id: int) -> str:
    """
    To check the entered password
    :param id: telegram id
    :return: password for verification
    """
    async with engine.connect() as conn:
        sql = await conn.execute(select(Users.personal_pass).where(Users.telegram_id == id))
        result: tuple = sql.fetchone()
    await engine.dispose()
    return result[0]


async def update_personal_pass(id: int, personal_pass: str):
    """
    Sets a new password for verification
    :param id: telegram id
    :param personal_pass: password
    """
    sql = update(Users).where(Users.telegram_id == id).values(personal_pass=personal_pass)
    async with AsyncSession(engine) as session:
        await session.execute(sql)
        await session.commit()
    await engine.dispose()


async def update_birthday(id: int, birthday) -> None:
    """
    Sets the values of the user's birthday.
    :param id: telegram id
    :param birthday: birthday date
    """
    sql = update(Users).where(Users.telegram_id == id).values(birthday=birthday)
    async with AsyncSession(engine) as session:
        await session.execute(sql)
        await session.commit()
    await engine.dispose()


async def select_user_birthday(id: int) -> str:
    """
    Selects a user by his ID
    :param id: telegram id
    :return: user info
    """
    async with engine.connect() as conn:
        result = await conn.execute(select(Users.birthday).where(Users.telegram_id == id))
    await engine.dispose()
    return result.fetchone()[0]
