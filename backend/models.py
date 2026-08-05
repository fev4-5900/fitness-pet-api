# SQLAlchemy models - one Python class per database table.
# Each class below maps directly to the table named in __tablename__.
from database import Base
from sqlalchemy import Column, Integer, ForeignKey, Boolean, String, Float, DateTime, Date


# The user's virtual pet (one pet per user)
class pet(Base):
    __tablename__ = 'pet'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('user.id'), unique=True)  # one pet per user
    name = Column(String)
    description = Column(String)
    color = Column(String)
    hunger = Column(Integer)
    hydration = Column(Integer)
    sleep = Column(Integer)
    exercise = Column(Boolean, default=False)


# Registered users + their fitness profile
class user(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String(100), unique=True)
    hashed_password = Column(String(100))  # never store plain passwords
    username = Column(String(100), unique=True)
    phone_number = Column(String(100))
    role = Column(String(100))

    # Fitness profile used by the targets calculator
    gender = Column(String(100))
    height = Column(Float)
    weight = Column(Float)
    age = Column(Integer)
    activity = Column(Integer)  # training days per week (0-7)
    goal = Column(String(100))  # lose / maintain / gain


# The user's saved daily targets (one row per user, updated not duplicated)
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
    water = Column(Float)  # daily water goal in liters


# One row = one logged meal. Many rows per user, grouped by date.
class meals(Base):
    __tablename__ = 'meals'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('user.id'))
    calories = Column(Integer)
    proteins = Column(Integer)
    carbs = Column(Integer)
    fats = Column(Integer)
    date = Column(Date)  # day the meal was eaten


# One row = one glass/cup of water (in liters)
class water(Base):
    __tablename__ = 'water'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('user.id'))
    liters = Column(Float)
    date = Column(Date)


# One row = one night of sleep
class sleep_hours(Base):
    __tablename__ = 'sleep_hours'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('user.id'))
    sleep_hours = Column(Float)
    date = Column(Date)


# One row = one steps update
class steps(Base):
    __tablename__ = 'steps'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('user.id'))
    steps = Column(Integer)
    date = Column(Date)


# The user's running lifetime score, incremented when a log earns points
class overall_points(Base):
    __tablename__ = 'overall_points'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('user.id'), unique=True)
    overall_points = Column(Integer)

