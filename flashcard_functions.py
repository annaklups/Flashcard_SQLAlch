from random import choices
import re

from db_user_functions import login
from db_flashcard_functions import create_flashcard, get_flashcard
from db_wage_functions import get_wages_for_draw, update_wages

def input_new_user(text, regexp):
    """Colleting input data for new user or for changing settings/ password. 
    Checking correctness of inputs from user with regexp"""
    newu = input(text)
    pattern = re.compile(regexp)
    res = pattern.search(newu)
    if res:
        return newu
    else:
        return False

def login_in():
    """Loggin into the system. Fetching data from db for next actions."""
    print("Please enter login and password to log in")
    your_login = input("Login: ")
    your_password = input("Password: ")
    user = login(your_login, your_password)
    if user:
        print(f"{your_login} logged in !")
        logged_flag = True
        return {'logged_flag': logged_flag, 
                'user_num': user.user_num, 
                'login': user.login, 
                'flash_amount': user.flash_amount, 
                'new_flash_amount': user.new_flash_amount
                }
    else:
        print("You login data is incorrect")
        logged_flag = False
        return {'logged_flag': logged_flag}

def add_flashcard():
    """Collecting inputs, creating and adding new flashcard to database"""
    newf_topic = input("What topic this flashcard refers to?: ")
    newf_pol = input("Provide polish verion of this word or sentence: ")
    newf_translate = input("Provide translation of this word or sentence: ")
    create_flashcard(newf_pol.lower(), newf_translate.lower(), newf_topic.lower())

def learning(login_data):
    """Learning module - first old flashcards then new flashcards"""
    learning_part(login_data, login_data['flash_amount'] - login_data['new_flash_amount'], False)
    learning_part(login_data, login_data['new_flash_amount'], True)

def learning_part(login_data, repetitions, flag_new):
    """One part of learning flashards (as many as previously declared in users data). 
    New or old ones. Updating wages based on users answers"""
    for i in range(repetitions):
        flash_drawn = draw_flashcard(login_data['user_num'], flag_new)
        wage_change = learn_flashcard(flash_drawn)
        update_wages(login_data['user_num'], flash_drawn.flash_num, wage_change)

def draw_flashcard(user_num, flag_new):
    """Drawing one flashcard from database based on user wages"""
    wages_all = get_wages_for_draw(user_num)
    # filter for old/new flashcards and reorder them -> [(flashcards_num), (wages)]
    wages_old = list(zip(*[pair for pair in wages_all if pair[1]!=5]))
    wages_new = list(zip(*[pair for pair in wages_all if pair[1]==5]))
    # drawing flashcard
    if (len(wages_old) > 0 and flag_new == False) or (len(wages_new) == 0):
        draw = choices(wages_old[0], wages_old[1], k=1)
    else:
        draw = choices(wages_new[0], k=1)     
    flash = get_flashcard(*draw)
    return flash
    # return {'pol': flash.pol, 'translate': flash.translate, 'topic': flash.topic, 'flash_num': flash.flash_num}

def learn_flashcard(flash_drawn):                
    """Learning flashard drawn previously from db. Returning wage update for the flashcard"""
    print(f"Flashcard number:{flash_drawn.flash_num} - POL: {flash_drawn.pol.upper()}")
    answer = input("Please provide translation:")
    if answer.lower() == flash_drawn.translate:
        print("Correct answer!!")
        return -1
    else:
        print(f"You have to work on that. Correct answer is: {flash_drawn.translate}")
        return 1