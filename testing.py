import sqlite3
from flashcard_functions import directory_path
from database import SessionLocal
from flashcard_models import User

conn = sqlite3.connect(directory_path("flashcards_db_alchemy.db"))
c = conn.cursor()

c.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(c.fetchall())
c.execute("SELECT * FROM users_tab;")
print(c.fetchall())

conn.commit()
conn.close()