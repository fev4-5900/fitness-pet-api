# Sets up the SQLAlchemy engine and session factory used by every router.
# Local development uses SQLite; production can point at PostgreSQL
# through the DATABASE_URL environment variable.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import DATABASE_URL

# SQLite needs check_same_thread=False because FastAPI uses multiple threads;
# PostgreSQL/other drivers don't need any special connect args.
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

# SessionLocal is the factory used to open a new DB session for each request
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Base is the parent class every model (table) inherits from
Base = declarative_base()
