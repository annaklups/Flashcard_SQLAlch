from database import SessionLocal
from flashcard_models import User, Flashcard, Wage

def create_user(newu_login, newu_password, newu_flash_amount, newu_new_flash_amount):
    db = SessionLocal()
    try:
        user = User(
            login=newu_login, 
            password=newu_password, 
            flash_amount=newu_flash_amount, 
            new_flash_amount=newu_new_flash_amount)
        db.add(user)
        db.commit() 
        user = db.query(User).filter(User.login == newu_login).first()
        flashcards = db.query(Flashcard).all()
        for flash in flashcards:
            wage = Wage(
                user_num = user.user_num,
                flash_num = flash.flash_num,
                score=5)
            db.add(wage)
        db.commit()        
    except:
        print(f"User with {newu_login} exist in database already")
    finally:
        db.close()

def get_all_users():
    db = SessionLocal()
    users = db.query(User).all()
    print(users)

def get_user(log_login):
    db = SessionLocal()
    user = db.query(User).filter(User.login == log_login).first()
    print(user)
    return user

def change_settings(log_login, cs_flash_amount, cs_new_flash_amount):
    db = SessionLocal()
    user = db.query(User).filter(User.login == log_login)
    user.update({
        User.flash_amount: cs_flash_amount,
        User.new_flash_amount: cs_new_flash_amount
    })
    db.commit()
    db.close()

def delete_user(log_login):
    db = SessionLocal()
    user = db.query(User).filter(User.login == log_login).first()
    db.delete(user)
    db.commit()
    db.close()

def change_password(log_login, new_password1):
    db = SessionLocal()
    user = db.query(User).filter(User.login == log_login)
    user.update({User.password: new_password1})
    db.commit()
    db.close()

create_user('ania1','pass', 9, 3)
# get_all_users()

# get_user('annak')
# change_settings('annak', 10, 2)
# delete_user('aniaa3456')
