from database import SessionLocal
from flashcard_models import Flashcard

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
    except:
        print(f"Flashcard with {newf_pol} word exist in database already")
    finally:
        db.close()

def get_all_flashcards():
    db = SessionLocal()
    flashcards = db.query(Flashcard).all()
    print(flashcards)


def add_flashcard():
    """Collecting inputs, creating and adding new flashcard to database"""
    newf_topic = input("What topic this flashcard refers to?: ")
    newf_pol = input("Provide polish verion of this word or sentence: ")
    newf_translate = input("Provide translation of this word or sentence: ")
    f = Flashcard(newf_pol.lower(), newf_translate.lower(), newf_topic.lower())
    f.add_1_flashcard_to_db()