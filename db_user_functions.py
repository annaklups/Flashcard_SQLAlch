from database import SessionLocal
from flashcard_models import User

def create_user(newu_login, newu_password, newu_flash_amount, newu_new_flash_amount):
    db = SessionLocal()
    user = User(
        login=newu_login, 
        password=newu_password, 
        flash_amount=newu_flash_amount, 
        new_flash_amount=newu_new_flash_amount)
    db.add(user)
    db.commit()
    db.close()

def change_settings():
    pass

def delete_user():
    pass

def change_password():
    pass

# czy change settings i change password muszą być osobno?





create_user('annak','blabla', 5, 4)