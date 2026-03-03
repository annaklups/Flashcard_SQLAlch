from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# flashcards_db_alchemy.db is the name od database:
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "flashcards_db_alchemy.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# engine creation
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# creating connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()