from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Path to the SQLite database file (created automatically in this folder)
sqlalchemy_database_url = "sqlite:///./fitness-pet.db"

# SQLite needs check_same_thread=False because FastAPI uses multiple threads
engine = create_engine(sqlalchemy_database_url, connect_args={"check_same_thread": False})

# SessionLocal is the factory used to open a new DB session for each request
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Base is the parent class every model (table) inherits from
Base = declarative_base()
