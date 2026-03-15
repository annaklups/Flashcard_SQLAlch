from database import SessionLocal
from flashcard_models import User, Flashcard, Wage

def get_wages_for_draw(user_num):
    db = SessionLocal()
    wages = db.query(Wage).filter(Wage.user_num == user_num).all()
    wage_list = []
    for wage in wages:
        wage_list.append((wage.flash_num, wage.score))
    print(wage_list)
    return wage_list

def update_wages(log_login, cs_flash_amount, cs_new_flash_amount):
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


get_wages_for_draw(1)
wages_all = get_wages_for_draw(1)
wages_old = [pair for pair in wages_all if pair[1]==5]
wages_pr = list(zip(*wages_old))
print(wages_pr)