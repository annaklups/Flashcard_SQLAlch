import sqlite3
from random import choices
import ast
import re

from flashcard_classes import Flashcard
from gen_functions import directory_path

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

    conn = sqlite3.connect(directory_path("flashcards_db.db"))
    c = conn.cursor()
    c.execute("SELECT * FROM users_tab WHERE login = ? AND password = ?", (your_login, your_password))
    db_record = c.fetchall()
    if db_record:
        print(f"{your_login} logged in !")
        logged_flag = True
        user_num, login, *password, flash_amount, new_flash_amount = db_record[0]
        # db record: list[tuple] - [(user_num, login, password, all_flash, new_flash)]
        conn.commit()
        conn.close()       
        return {'logged_flag': logged_flag, 'user_num': user_num, 'login': login, 'flash_amount': flash_amount, 'new_flash_amount': new_flash_amount}
    else:
        print(f"You login data is incorrect")
        logged_flag = False
        conn.commit()
        conn.close()
        return {'logged_flag': logged_flag}    

def add_flashcard():
    """Collecting inputs, creating and adding new flashcard to database"""
    newf_topic = input("What topic this flashcard refers to?: ")
    newf_pol = input("Provide polish verion of this word or sentence: ")
    newf_translate = input("Provide translation of this word or sentence: ")
    f = Flashcard(newf_pol.lower(), newf_translate.lower(), newf_topic.lower())
    f.add_1_flashcard_to_db()

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
    conn = sqlite3.connect(directory_path("flashcards_db.db"))
    c = conn.cursor()
    c.execute("SELECT wages FROM users_info_tab WHERE user_num = ?", (user_num,))
    str_wages, = c.fetchall()[0]
    # creating dict of flashcard wages - dict{flashcard_num: wage}
    wages = ast.literal_eval(str_wages)
    # filtering for old/new flashcards
    wages_old = {k:v for k,v in wages.items() if v!=5}
    wages_new = {k:v for k,v in wages.items() if v==5}
    if (len(wages_old) > 0 and flag_new == False) or (len(wages_new) == 0):
        draw = choices(list(wages_old.keys()), list(wages_old.values()), k=1)
        # draw: list[] with k=1 elements
    else:
        draw = choices(list(wages_new.keys()), k=1)
    c.execute("SELECT * FROM flashcards_tab WHERE flash_num = ?", (draw[0],))
    flashcard_drawn = c.fetchall()
    flash_num, pol, translate, topic = flashcard_drawn[0]
    # flashcard_drawn: list[tuple]
    conn.commit()
    conn.close()
    return {'pol': pol, 'translate': translate, 'topic': topic, 'flash_num': flash_num, 'wages': wages}

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