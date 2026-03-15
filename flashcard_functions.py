import sqlite3
from random import choices
import re

from flashcard_classes import Flashcard
from gen_functions import directory_path

from db_flashcard_functions import create_flashcard, get_flashcard
from db_user_functions import login
from db_wage_functions import get_wages_for_draw


def input_new_user(text, regexp):
    """Colleting input data for new user or for changing settings/ password. Checking correctness of inputs from user"""
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
        return {'logged_flag': logged_flag, 'user_num': user.user_num, 'login': user.login, 'flash_amount': user.flash_amount, 'new_flash_amount': user.new_flash_amount}
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

def learning_part(login_data, repetitions, flag_new):                
    """Learning flashards (as many as previously declared in users data). Updating wages based on users answers"""
    for i in range(repetitions):
        flash_drawn = draw_flashcard(login_data['user_num'], flag_new)
        fd = Flashcard(flash_drawn['pol'], flash_drawn['translate'], flash_drawn['topic'], flash_drawn['flash_num'])
        wage_change = fd.learn_flashcard()
        print(flash_drawn['wages'], flash_drawn['flash_num'], wage_change)
        update_wages(login_data['user_num'], flash_drawn['wages'], flash_drawn['flash_num'], wage_change)
    
def learning(login_data):
    learning_part(login_data, login_data['flash_amount'] - login_data['new_flash_amount'], False)
    learning_part(login_data, login_data['new_flash_amount'], True)

def draw_flashcard(user_num, flag_new):
    """Drawing one flashcard from database"""
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
    return {'pol': flash.pol, 'translate': flash.translate, 'topic': flash.topic, 'flash_num': flash.flash_num}

def update_wages(user_num, wages, flash_num, change):
    """Updating user's wages in database based on his answer"""
    if wages[flash_num] == 1 and change == -1:
        pass
    else:
        wages[flash_num] = wages[flash_num] + change
        conn = sqlite3.connect(directory_path("flashcards_db.db"))
        c = conn.cursor()
        c.execute("UPDATE users_info_tab SET wages = ? WHERE user_num = ?;", (str(wages), user_num))        
        conn.commit()
        conn.close()

draw_flashcard(1, False)