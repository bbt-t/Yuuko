from sqlalchemy import Column, VARCHAR, PickleType, BigInteger, Date, ForeignKey, DateTime, Enum, TEXT
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func

from loader import Base
from utils.misc.enums_data import BotSkins


class Users(Base):
    __tablename__ = 'users'

    telegram_id = Column(BigInteger, primary_key=True, index=True)
    __personal_pass = Column(VARCHAR(32), index=True)
    birthday = Column(Date, nullable=True)
    __email = Column(VARCHAR(128), nullable=True, unique=True)
    full_username = Column(VARCHAR(64), nullable=True)
    selected_bot_skin = Column(
        Enum(BotSkins),
        nullable=True,
        index=True,
        default=getattr(BotSkins, 'chan'),
        doc="If not selected when first launching the bot, "
            "it is automatically selected (by default) 'Chan' sticker pack."
    )
    selected_bot_lang = Column(VARCHAR(2), index=True, default='en')
    created_time = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_time = Column(DateTime(timezone=True), onupdate=func.now())

    @hybrid_property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email

    @hybrid_property
    def personal_pass(self):
        return self.__personal_pass

    @personal_pass.setter
    def personal_pass(self, personal_pass):
        self.__personal_pass = personal_pass


class OtherInfo(Base):
    __tablename__ = 'other'

    telegram_id = Column(BigInteger, ForeignKey("users.telegram_id", ondelete='CASCADE'))
    __name_pass = Column(VARCHAR(32), primary_key=True, index=True, doc="Requested password name.")
    __pass_item = Column(PickleType, nullable=False)
    created_time = Column(DateTime(timezone=True), server_default=func.now())
    updated_time = Column(DateTime(timezone=True), onupdate=func.now())

    @hybrid_property
    def name_pass(self):
        return self.__name_pass

    @name_pass.setter
    def name_pass(self, name):
        self.__name_pass = name

    @hybrid_property
    def pass_item(self):
        return self.__pass_item

    @pass_item.setter
    def pass_item(self, item):
        self.__pass_item = item


class UsersRecipes(Base):
    __tablename__ = 'usersrecipes'

    telegram_id = Column(BigInteger, ForeignKey("users.telegram_id", ondelete='CASCADE'))
    name = Column(VARCHAR(32), primary_key=True, index=True)
    ingredients = Column(TEXT, nullable=False)
    recipe = Column(TEXT, nullable=False)
    created_time = Column(DateTime(timezone=True), server_default=func.now())
    updated_time = Column(DateTime(timezone=True), onupdate=func.now())