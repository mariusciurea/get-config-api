"""Database connection and operations for the get_config_api

DB_URL = dialect+driver://username:password@host:port/database

DB_URL_MYSQL =  mysql+pymysql://root:Changeme_123@localhost:3306/devgetconfig
DB_URL_POSTGRES =  postgresql+psycopg2://username:password@host:port/database
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from src.get_config_api.settings import get_db_settings


db_settings = get_db_settings()

db_url = f"mysql+pymysql://{db_settings.DB_USER}:{db_settings.DB_PASSWORD}@{db_settings.DB_HOST}:{db_settings.DB_PORT}/{db_settings.DB_NAME}"

engine = create_engine(db_url)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()