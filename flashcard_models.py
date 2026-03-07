from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from database import Base

class User(Base):
    __tablename__ = 'users_tab'

    user_num: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(20), unique=True)
    password: Mapped[str] = mapped_column(String(20))
    flash_amount: Mapped[int] = mapped_column(Integer)
    new_flash_amount: Mapped[int] = mapped_column(Integer)
    # wages = relationship("Wages", back_populates ='scores')

    def __repr__(self):
        return f"User {self.user_num} login {self.login}"

class Flashcard(Base):
    __tablename__ = 'flashcards_tab'

    flash_num: Mapped[int] = mapped_column(primary_key=True)
    pol: Mapped[str] = mapped_column(String(50), unique=True)
    translate: Mapped[str] = mapped_column(String(50))
    topic: Mapped[str] = mapped_column(String(20))

    def __repr__(self):
        return f"Flashcard: {self.flash_num}: {self.pol} - {self.translate}"

class Wages(Base):
    __tablename__ = 'wages_tab'

    user_num: Mapped[int] = mapped_column(ForeignKey("users_tab.user_num"), primary_key=True)
    flash_num: Mapped[int] = mapped_column(ForeignKey("flashcards_tab.flash_num"), primary_key=True)
    score: Mapped[int] = mapped_column(Integer, default=0)
    # scores = relationship("User", back_populates='wages')

