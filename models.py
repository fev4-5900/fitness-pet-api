from database import Base
from sqlalchemy import Column, Integer, ForeignKey, Boolean, String


class pet(Base):
    __tablename__ = 'pet'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('user.id'))
    name = Column(String)
    description = Column(String)
    color = Column(String)
    hunger = Column(Integer)
    hydration = Column(Integer)
    sleep = Column(Integer)
    exercise = Column(Boolean, default=False)





class user(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String(100),unique=True)
    hashed_password = Column(String(100))
    username = Column(String(100),unique=True)
    phone_number = Column(String(100))
