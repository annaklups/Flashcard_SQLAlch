from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Text
from database import Base

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


# models.py:
# from sqlalchemy.sql.sqltypes import Integer, String, Boolean
# from sqlalchemy.sql.schema import ForeignKey
# from sqlalchemy.orm import relationship
# from db.database import Base
# from sqlalchemy import Column

# class DbUser(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String)
#     email = Column(String)
#     password = Column(String)
#     items = relationship('DbArticle', back_populates = 'user')

# class DbArticle(Base):
#     __tablename__='articles'
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String)
#     content = Column(String)
#     published = Column(Boolean)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     user = relationship("DbUser", back_populates ='items')