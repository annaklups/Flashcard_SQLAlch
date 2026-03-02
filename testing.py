import sqlite3
from flashcard_functions import directory_path
from database import SessionLocal
from flashcard_models import User

db = SessionLocal()
user1 = User(login='anna', password='pass1234', flash_amount=4, new_flash_amount=2)
db.add(user1)
db.commit()
db.close()

conn = sqlite3.connect(directory_path("flashcards_db_alchemy.db"))
c = conn.cursor()

c.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(c.fetchall())
c.execute("SELECT * FROM users_tab;")
print(c.fetchall())

conn.commit()
conn.close()