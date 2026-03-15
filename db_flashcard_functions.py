from database import SessionLocal
from flashcard_models import Flashcard, User, Wage

def create_flashcard(newf_pol, newf_translate, newf_topic):
    db = SessionLocal()
    try:
        flashcard = Flashcard(
            pol = newf_pol,
            translate = newf_translate,
            topic = newf_topic
        )
        db.add(flashcard)
        db.commit()
        flashcard = db.query(Flashcard).filter(Flashcard.pol == newf_pol).first()
        users = db.query(User).all()
        for user in users:
            wage = Wage(
                user_num = user.user_num,
                flash_num = flashcard.flash_num,
                score=5)
            db.add(wage)            
        db.commit()
        print(f"Flashcard {flashcard.flash_num}: {flashcard.pol} added to database")        
    except:
        print(f"Flashcard with {newf_pol} word exist in database already")
    finally:
        db.close()

def get_all_flashcards():
    db = SessionLocal()
    flashcards = db.query(Flashcard).all()
    print(flashcards)

def get_flashcard(flashcard_number):
    db = SessionLocal()
    flashcard = db.query(Flashcard).filter(Flashcard.flash_num == flashcard_number).first()
    print(flashcard)
    return flashcard


create_flashcard('szafa','drawer','everyday objects')
# get_all_flashcards()
# get_flashcard(1)