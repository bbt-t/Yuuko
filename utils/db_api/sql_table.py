from sqlalchemy import Column, String, PickleType, SmallInteger, Boolean

from loader import Base




class Users(Base):
    __tablename__ = 'users'
    telegram_id = Column(SmallInteger, primary_key=True)
    full_name = Column(String)
    weather_notif_status = Column(Boolean)
    todo_notif_status = Column(Boolean)
    personal_pass = Column(String)


class OtherInfo(Base):
    __tablename__ = 'other'
    telegram_id = Column(SmallInteger, primary_key=True)
    name_pass = Column(String, nullable=False, unique=True)
    pass_items = Column(PickleType, nullable=False)