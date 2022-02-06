from sqlalchemy import Column, VARCHAR, PickleType, BigInteger, Date, ForeignKey, DateTime, Enum
from sqlalchemy.sql import func

from loader import Base
from utils.misc.enums_data import BotSkins


class Users(Base):
    __tablename__ = 'users'
    telegram_id = Column(BigInteger, primary_key=True)
    personal_pass = Column(VARCHAR(32))
    birthday = Column(Date, nullable=True)
    email = Column(VARCHAR(128), nullable=True)
    full_username = Column(VARCHAR(128), nullable=True)
    selected_bot_skin = Column(Enum(BotSkins), nullable=True)
    selected_bot_lang = Column(VARCHAR(2), nullable=True)
    created_time = Column(DateTime(timezone=True), server_default=func.now())
    updated_time = Column(DateTime(timezone=True), onupdate=func.now())


class OtherInfo(Base):
    __tablename__ = 'other'
    telegram_id = Column(BigInteger, ForeignKey("users.telegram_id"))
    name_pass = Column(VARCHAR(256), primary_key=True)
    pass_items = Column(PickleType, nullable=False)
    created_time = Column(DateTime(timezone=True), server_default=func.now())
    updated_time = Column(DateTime(timezone=True), onupdate=func.now())
