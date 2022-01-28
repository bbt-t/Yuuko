from sqlalchemy import Column, VARCHAR, PickleType, BigInteger, Date, Boolean

from loader import Base


class Users(Base):
    __tablename__ = 'users'
    telegram_id = Column(BigInteger, primary_key=True)
    personal_pass = Column(VARCHAR(32))
    birthday = Column(Date, nullable=True)


class OtherInfo(Base):
    __tablename__ = 'other'
    telegram_id = Column(BigInteger, nullable=False)
    name_pass = Column(VARCHAR(256), primary_key=True)
    pass_items = Column(PickleType, nullable=False)
