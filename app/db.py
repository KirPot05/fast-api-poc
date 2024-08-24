from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import os


load_dotenv()

URL = os.getenv("DB_URL")
if URL is None:
    raise Exception("DB_URL not specified")

engine = create_engine(
    url=URL)

Session = sessionmaker(autocommit=False, bind=engine, autoflush=False)
Base = declarative_base()


def get_db_connection():
    db = Session()

    try:
        yield db
    finally:
        db.close()
