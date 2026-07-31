from database import Base
from sqlalchemy import Column, Integer, ForeignKey, Boolean, String, Float
from datetime import datetime

class pet(Base):
    __tablename__ = 'pet'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('user.id'), unique=True)
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
    role = Column(String(100))

    gender = Column(String(100))
    height = Column(Float)
    weight = Column(Float)
    age = Column(Integer)
    activity = Column(Integer)
    goal = Column(String(100))



class user_targets(Base):
    __tablename__ = 'user_targets'


    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('user.id'), unique=True)
    calories = Column(Integer)
    proteins = Column(Integer)
    carbs = Column(Integer)
    fats = Column(Integer)
    sleep_hours = Column(Integer)
    steps = Column(Integer)

class meals(Base):
    __tablename__ = 'meals'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('user.id'), unique=True)
    calories = Column(Integer)
    proteins = Column(Integer)
    carbs = Column(Integer)
    fats = Column(Integer)
    date = Column(datetime.day)


class water(Base):
    __tablename__ = 'water'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('user.id'), unique=True)
    liters = Column(float)


class sleep_hours(Base):
    __tablename__ = 'sleep_hours'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('user.id'), unique=True)
    sleep_hours = Column(Float)
    date = Column(datetime.day)

class steps(Base):
    __tablename__ = 'steps'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('user.id'), unique=True)
    steps = Column(Integer)
    date = Column(datetime.day)





