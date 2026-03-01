# Models
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Text

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users_tab'

    user_num: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(20))
    password: Mapped[str] = mapped_column(String(20))
    flash_amount: Mapped[int] = mapped_column(Integer)
    new_flash_amount: Mapped[int] = mapped_column(Integer)
    # wages: Mapped[dict] = mapped_column(Text)

    def __repr__(self):
        return f"User {self.user_num} login {self.login}"


# Engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# sessionmaker - czy napewno potrzebne? sprawdzić

SQLALCHEMY_DATABASE_URL = "sqlite:///./flashcard_sqlalch.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind = engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 
# Create database
Base.metadata.create_all(engine)


