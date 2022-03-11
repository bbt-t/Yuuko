from enum import Enum
from pickle import loads as pickle_loads
from typing import final

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import Update, Delete

from loader import Base, engine
from .sql_table import OtherInfo, Users, UsersRecipes


async def start_db() -> None:
    """
    Drop and Create table
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@final
class DataBaseUsersInfo:

    user_general_info = Users
    user_other_info = OtherInfo
    user_recipes = UsersRecipes

    @staticmethod
    async def _database_query(sql, is_add: bool = None, is_select: bool = None):
        if is_add:
            async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
            async with async_session() as session:
                async with session.begin():
                    session.add(sql)
                await session.commit()
        elif is_select:
            async with engine.connect() as conn:
                result = await conn.execute(sql)
            return result
        else:
            async with AsyncSession(engine) as session:
                await session.execute(sql)
                await session.commit()
        await engine.dispose()

    async def add_user(self, telegram_id: int, lang: str = 'ru') -> None:
        """
        Add user in table 'Users'
        :param telegram_id: telegram id
        :param lang: device language
        """
        if lang is None:
            lang = 'ru'
        user = self.user_general_info(telegram_id=telegram_id, selected_bot_lang=lang)
        await self._database_query(is_add=True, sql=user)

    async def add_other_info(self, telegram_id: int, name: str, info_for_save: bytes) -> None:
        """
        Adds an encrypted password in table 'Others_info'
        :param telegram_id: telegram user id
        :param name: password name
        :param info_for_save: password
        """
        sql = self.user_other_info(telegram_id=telegram_id, name_pass=name, pass_item=info_for_save)
        await self._database_query(is_add=True, sql=sql)

    async def add_recipe(self, telegram_id: int | str, name: str, ingredients: str | list, recipe: str) -> None:
        """
        Add recipe.
        :param telegram_id: telegram user id
        :param name: selected recipe-name
        :param ingredients: recipe ingredients
        :param recipe: recipe
        """
        sql = self.user_recipes(telegram_id=telegram_id, name=name, ingredients=ingredients, recipe=recipe)
        await self._database_query(is_add=True, sql=sql)

    async def update_pass(self, telegram_id: int, name_pass: str, info_for_save: bytes) -> None:
        """
        Sets a new password for verification
        :param telegram_id: telegram user id
        :param name_pass: password name to change
        :param info_for_save: password
        """
        sql = Update(self.user_other_info).where(
            self.user_other_info.telegram_id == telegram_id, self.user_other_info.name_pass == name_pass
        ).values(pass_item=info_for_save)
        await self._database_query(sql=sql)

    async def update_personal_pass(self, telegram_id: int | str, personal_pass: str | None) -> None:
        """
        Sets a new codeword for verification.
        :param telegram_id: telegram user id
        :param personal_pass: password
        """
        sql = Update(
            self.user_general_info).where(
            self.user_general_info.telegram_id == telegram_id).values(personal_pass=personal_pass)
        await self._database_query(sql=sql)

    async def update_birthday(self, telegram_id: int | str, birthday) -> None:
        """
        Sets the values of the user's birthday.
        :param telegram_id: telegram user id
        :param birthday: birthday date
        """
        sql = Update(
            self.user_general_info).where(
            self.user_general_info.telegram_id == telegram_id).values(birthday=birthday)
        await self._database_query(sql=sql)

    async def update_recipe_photo(self, telegram_id: int | str, name: str, photo_url: str) -> None:
        """
        Sets the values of the recipes photo.
        :param telegram_id: telegram user id
        :param name: recipe name
        :param photo_url: url in telegram
        """
        sql = Update(
            self.user_recipes).where(
            self.user_recipes.telegram_id == telegram_id, self.user_recipes.name == name).values(recipe_photo_url=photo_url)
        await self._database_query(sql=sql)

    async def update_bot_language(self, telegram_id: int | str, lang: str) -> None:
        """
        Changes the language of the bot.
        :param telegram_id: telegram user id
        :param lang: language
        """
        sql = Update(
            self.user_general_info).where(
            self.user_general_info.telegram_id == telegram_id).values(selected_bot_lang=lang)
        await self._database_query(sql=sql)

    async def update_bot_skin(self, telegram_id: int | str, skin: str) -> None:
        """
        Changes the skin of the bot.
        :param telegram_id: telegram user id
        :param skin: user-selected skin
        """
        sql = Update(
            self.user_general_info).where(
            self.user_general_info.telegram_id == telegram_id).values(selected_bot_skin=skin)
        await self._database_query(sql=sql)

    async def delete_user(self, telegram_id: int | str) -> None:
        """
        Delete a user by his ID.
        :param telegram_id: telegram user id
        :return: user info
        """
        sql = Delete(self.user_general_info).where(self.user_general_info.telegram_id == telegram_id)
        await self._database_query(sql=sql)

    async def check_personal_pass(self, telegram_id: int | str) -> str:
        """
        To check the entered codeword.
        :param telegram_id: telegram user id
        :return: password for verification
        """
        sql = select(self.user_general_info.personal_pass).where(self.user_general_info.telegram_id == telegram_id)
        result = await self._database_query(is_select=True, sql=sql)
        return result.scalar_one()

    async def select_pass(self, telegram_id: int | str, name: str) -> str:
        """
        Gets password and extracts from pkl.
        :param telegram_id: telegram user id
        :param name: saved password name
        :return: password
        """
        sql = select(
            self.user_other_info.pass_item).where(
            self.user_other_info.telegram_id == telegram_id, self.user_other_info.name_pass == name)
        result = await self._database_query(is_select=True, sql=sql)
        return pickle_loads(result.scalar_one())

    async def select_user(self, telegram_id: int | str) -> tuple:
        """
        Selects a user by his ID.
        :param telegram_id: telegram user id
        :return: user info
        """
        sql = select(self.user_general_info).where(self.user_general_info.telegram_id == telegram_id)
        result = await self._database_query(is_select=True, sql=sql)
        return result.fetchone()

    async def select_all_users(self) -> list:
        """
        Selects all users telegram id.
        :return: all telegram id in list
        """
        sql = select(self.user_general_info.telegram_id)
        result = await self._database_query(is_select=True, sql=sql)
        return result.scalars().all()

    async def select_user_birthday(self, telegram_id: int | str) -> str:
        """
        Selects a user's birthday by their telegram id.
        :param telegram_id: telegram user id
        :return: user info
        """
        sql = select(self.user_general_info.birthday).where(self.user_general_info.telegram_id == telegram_id)
        result = await self._database_query(is_select=True, sql=sql)
        return result.scalar_one()

    async def select_skin(self, telegram_id: int | str):
        """
        Selects the selected bot-skin by user telegram id.
        :param telegram_id: telegram user id
        :return: user info in enum
        """
        sql = select(self.user_general_info.selected_bot_skin).where(self.user_general_info.telegram_id == telegram_id)
        result = await self._database_query(is_select=True, sql=sql)
        return result.scalar_one().value

    async def select_bot_language(self, telegram_id: int | str) -> str:
        """
        Selects the selected language by user telegram id.
        :param telegram_id: telegram user id
        :return: user info in enum
        """
        sql = select(self.user_general_info.selected_bot_lang).where(self.user_general_info.telegram_id == telegram_id)
        result = await self._database_query(is_select=True, sql=sql)
        return result.scalar_one()

    async def select_lang_and_skin(self, telegram_id: int | str) -> tuple[str, Enum]:
        """
        Select language and skin
        """
        sql = select(
            self.user_general_info.selected_bot_lang, self.user_general_info.selected_bot_skin).where(
            self.user_general_info.telegram_id == telegram_id)
        result = await self._database_query(is_select=True, sql=sql)
        lang, skin = result.one()
        return lang, skin.value

    async def check_invalid_user(self, telegram_id: int) -> bool:
        """
        Сhecks the user by his telegram id.
        :param telegram_id: telegram user id
        :return: True or False
        """
        sql = select(self.user_general_info.created_time).where(self.user_general_info.telegram_id == telegram_id)
        result = await self._database_query(is_select=True, sql=sql)
        return not result.one_or_none()

    async def select_recipe(self, telegram_id: int | str, name: str) -> tuple | None:
        """
        Selects recipe by user telegram id.
        :param telegram_id: telegram user id
        :param name: recipe name
        :return: recipe
        """
        sql = select(self.user_recipes.ingredients, self.user_recipes.recipe).where(
            self.user_recipes.telegram_id == telegram_id, self.user_recipes.name == name)
        result = await self._database_query(is_select=True, sql=sql)

        return result.one_or_none()


DB_USERS = DataBaseUsersInfo()
