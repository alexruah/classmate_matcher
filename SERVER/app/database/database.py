import os
from dotenv import load_dotenv

from sqlmodel import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")


engine = create_engine(DB_URL)

SesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SesionLocal()
    try:
        yield db
    finally:
        db.close()