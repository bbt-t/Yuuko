from sqlalchemy import Column, VARCHAR, PickleType, BigInteger, Boolean, Date

from loader import Base




class Users(Base):
    __tablename__ = 'users'
    telegram_id = Column(BigInteger, primary_key=True)
    full_name = Column(VARCHAR(256), nullable=False)
    todo_notif_status = Column(Boolean)
    personal_pass = Column(VARCHAR(32))
    birthday = Column(Date)


class OtherInfo(Base):
    __tablename__ = 'other'
    telegram_id = Column(BigInteger, primary_key=True)
    name_pass = Column(VARCHAR(256), nullable=False, unique=True)
    pass_items = Column(PickleType, nullable=False)