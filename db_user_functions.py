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
        print(f"User {newu_login} added to db")        
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
    return user

def login(log_login, password):
    db = SessionLocal()
    user = db.query(User).filter(User.login == log_login, User.password == password).first()
    return user    

def change_settings(log_login, cs_flash_amount, cs_new_flash_amount):
    try:
        db = SessionLocal()
        user = db.query(User).filter(User.login == log_login)
        user.update({
            User.flash_amount: cs_flash_amount,
            User.new_flash_amount: cs_new_flash_amount
        })
        db.commit()
        print("Settings changed correctly")
    except:
        print("Error occured")
    finally:
        db.close()

def delete_user(log_login):
    try:
        db = SessionLocal()
        user = db.query(User).filter(User.login == log_login).first()
        db.delete(user)
        db.commit()
        print(f"User {log_login} delete from database")
    except:
        print("Error occured")
    finally:
        db.close()

def change_password(log_login, new_password1):
    try:
        db = SessionLocal()
        user = db.query(User).filter(User.login == log_login)
        user.update({User.password: new_password1})
        db.commit()
        print("Password changed correctly")
    except:
        print("Error occured")
    finally:
        db.close()


# create_user('ania1','pass', 9, 3)
# get_all_users()
# get_user('AniaK')
# get_user("buba")
login('AniaK', 'Qwerty2')
# change_settings('annak', 10, 2)
# delete_user('aniaa3456')
