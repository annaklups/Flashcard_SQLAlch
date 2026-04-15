from database import SessionLocal
from flashcard_models import Wage
from sqlalchemy import select, update

def get_wages_for_draw(user_number):
    """Getting wages from db for selected user. Returning list of wages."""
    db = SessionLocal()
    wages = db.scalars(select(Wage).filter_by(user_num = user_number))
    wage_list = []
    for wage in wages:
        wage_list.append((wage.flash_num, wage.score))
    print(wage_list)
    return wage_list

def update_wages(user_number, flash_number, wage_change):
    """Updating wage for selected user and flashcard with provided wage change"""
    try:
        db = SessionLocal()
        wage_to_update = db.scalars(select(Wage).filter_by(user_num = user_number, flash_num = flash_number)).first()
        new_wage = wage_to_update.score + wage_change
        db.execute(update(Wage).where(Wage.user_num == user_number, Wage.flash_num == flash_number).values(score = new_wage))
        db.commit()
    except:
        print("Error with wage updated occured")
    finally:
        db.close()

# get_wages_for_draw(1)