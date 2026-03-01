"""Flashcards learning program"""

# Import
import sqlite3
from csv import reader
import re

from flashcard_classes import User, Flashcard, Choice


# Creating basic tables
conn = sqlite3.connect(directory_path("flashcards_db.db"))
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users_tab (user_num INTEGER PRIMARY KEY, login TEXT, password TEXT, flash_amount INT, new_flash_amount INT);")
c.execute("CREATE TABLE IF NOT EXISTS users_info_tab (user_num INTEGER PRIMARY KEY, wages TEXT);")
c.execute("CREATE TABLE IF NOT EXISTS flashcards_tab (flash_num INTEGER PRIMARY KEY, pol TEXT, translate TEXT, topic TEXT);")
# For developing phase only:
c.execute("DELETE FROM flashcards_tab")
# c.execute("DELETE FROM users_tab")
conn.commit()
conn.close()

# Adding basic pack of flashcards to database
with open(directory_path("flashcards_csv.csv"), encoding='utf-8') as file:
    csv_reader = reader(file)
    flashcards_source = list(csv_reader)
   
    for line in flashcards_source:            
        f = Flashcard(line[0], line[1], line[2])
        f.add_1_flashcard_to_db()

# For developing phase only:
conn = sqlite3.connect(directory_path("flashcards_db.db"))
c = conn.cursor()
# c.execute("SELECT * FROM flashcards_tab;")
# print(c.fetchall())
c.execute("SELECT * FROM users_tab;")
print(c.fetchall())    
c.execute("SELECT * FROM users_info_tab;")
print(c.fetchall())
conn.commit()
conn.close()

# Main menu 
print("Hi, This is your new flashcard learning program!")
while True:
    user_choice = int(input(
        "What do you wish to do? (type number):  \n " \
        "1 - create new user \n " \
        "2 - change settings for existing user \n " \
        "3 - change password for existing user \n " \
        "4 - delete user \n " \
        "5 - log in to existing account and start learning \n " \
        "6 - add your own flashcards \n "  \
        "7 - close the program \n"))

# 1. creating new user
    if user_choice == Choice.create_new_user:
        while True:
            newu_login = input("New user login (use letters only): ")
            pattern_login = re.compile(r'^[A-Za-z]+$')
            res_login = pattern_login.search(newu_login)
            if not res_login:
                print('Please, use only letters')
                continue
            break

        while True:
            newu_password = input("Password (use at least 1 uppercase letter, 1 lowercase letter, 1 digit): ")
            pattern_password = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')
            res_password = pattern_password.search(newu_password)
            if not res_password:
                print('Please, use (at least) 1 uppercase letter, 1 lowercase letter, 1 digit')
                continue
            break

        while True:        
            newu_flash_amount = input("How many flashcard do you want to train per session?: ")
            pattern_flash = re.compile(r'^[0-9]+$')
            res_flash = pattern_flash.search(newu_flash_amount)
            if not res_flash:
                print('Please, provide number of flashcards')
                continue
            break
        
        while True:
            newu_new_flash_amount = input("How many of them you want to be completely new? (must be less than your previous answer): ")
            res_flash = pattern_flash.search(newu_new_flash_amount)
            if not res_flash or (newu_new_flash_amount < newu_flash_amount):
                print('Please, provide correct number of new flashcards')
                continue
            break     

        nu = User(newu_login, newu_password, newu_flash_amount, newu_new_flash_amount)
        nu.create_user()

# 2. change settings for existing user
    elif user_choice == Choice.change_settings:    
        print("Please login first to change settings")
        while True:
            login_data = loggin_in()
            if login_data['logged_flag'] == True:
                cs_flash_amount = input("How many flashcard do you want to train per session?: ")
                cs_new_flash_amount = input("How many of them you want to be completely new?: ")
                cs = User(login_data['login'], "dummy_password", cs_flash_amount, cs_new_flash_amount, login_data['user_num'])
                cs.change_settings()
                break        
            else:
                print("To change the settings you need to first log in correctly")
                main_back = input("Do you wish to go back to main menu? (Y/N) ")
                if main_back in ('yes', 'YES', 'Yes', 'y', 'Y'):
                    break

# 3. change password for existing user
    elif user_choice == Choice.change_password:
        print("Please login first to change the password")
        main_back = 'N'
        while main_back not in ('yes', 'YES', 'Yes', 'y', 'Y'):
            login_data = loggin_in()
            if login_data['logged_flag'] == True:
                while main_back not in ('yes', 'YES', 'Yes', 'y', 'Y'):
                    new_password1 = input("Provide new password: ")
                    new_password2 = input("Provide new password: ")
                    if new_password1 == new_password2:
                        cs = User(login_data['login'], new_password1, login_data['flash_amount'], login_data['new_flash_amount'], login_data['user_num'])
                        cs.change_password()
                        main_back = 'Y'
                    else:
                        print("New passwords are not identical!")
                        main_back = input("Do you wish to go back to main menu? (Y/N) ")
            else:
                print("To change the password you need to first log in correctly")
                main_back = input("Do you wish to go back to main menu? (Y/N) ")

# 4. delete user
    elif user_choice == Choice.delete_user:
        print("Please login first to delete the account")
        while True:
            login_data = loggin_in()
            if login_data['logged_flag'] == True:        
                confirmation = input(f"Are you sure you want to delete {login_data['login']}? (Y/N) ")
                if confirmation in ('yes', 'YES', 'Yes', 'y', 'Y'):
                    dlt = User(login_data['login'], "dummy_password", login_data['flash_amount'], login_data['new_flash_amount'], login_data['user_num'])
                    dlt.delete_user()   
                    break
                else:
                    break     
            else:
                print("To delete the account you need to first log in correctly")
                main_back = input("Do you wish to go back to main menu? (Y/N) ")
                if main_back in ('yes', 'YES', 'Yes', 'y', 'Y'):
                    break                

# 5. log in to existing account and start learning
    elif user_choice == Choice.learning:
        continue_learning = 'Yes'
        while continue_learning in ('yes', 'YES', 'Yes', 'y', 'Y'):
            login_data = loggin_in()
            if login_data['logged_flag'] == True:
                while continue_learning in ('yes', 'YES', 'Yes', 'y', 'Y'):
                # learning old flashards - loop for number of old flashcards declared
                    for i in range(login_data['flash_amount']-login_data['new_flash_amount']):
                        flash_drawn = draw_flashcard(login_data['user_num'], flag_new=False)
                        fd = Flashcard(flash_drawn['pol'], flash_drawn['translate'], flash_drawn['topic'], flash_drawn['flash_num'])
                        wage_change = fd.learn_flashcard()
                        print(login_data['user_num'], flash_drawn['wages'], flash_drawn['flash_num'], wage_change)
                        update_wages(login_data['user_num'], flash_drawn['wages'], flash_drawn['flash_num'], wage_change)
                # learning new flashcards
                    for i in range(login_data['new_flash_amount']):
                        flash_drawn = draw_flashcard(login_data['user_num'], flag_new=True)
                        fd = Flashcard(flash_drawn['pol'], flash_drawn['translate'], flash_drawn['topic'], flash_drawn['flash_num'])
                        wage_change = fd.learn_flashcard()
                        print(login_data['user_num'], flash_drawn['wages'], flash_drawn['flash_num'], wage_change)
                        update_wages(login_data['user_num'], flash_drawn['wages'], flash_drawn['flash_num'], wage_change)
                    continue_learning = input("Do you wish to continue learning? (Y/N) ")
            else:
                print("To start learning you need to first log in correctly")
                main_back = input("Do you wish to go back to main menu? (Y/N) ")
                if main_back in ('yes', 'YES', 'Yes', 'y', 'Y'):
                    break     

# 6. add your own flashcard
    elif user_choice == Choice.add_flashcard:
        another_flashcard = 'yes'
        while another_flashcard in ('yes', 'YES', 'Yes', 'y', 'Y'):
            newf_topic = input("What topic this flashcard refers to?: ")
            newf_pol = input("Provide polish verion of this word or sentence: ")
            newf_translate = input("Provide translation of this word or sentence: ")
            f = Flashcard(newf_pol.lower(), newf_translate.lower(), newf_topic.lower())
            f.add_1_flashcard_to_db()
            another_flashcard = input("Do you want to add another flashcard? (Y/N) ")


# 7. exit the program
    elif user_choice == Choice.exit:
        print("Thank you for learning languages with us. See you soon!")
        break

# 99. testing mode 
    elif user_choice == 99 :
        print("test mode")

# To do:
#- przejść na sqlalchemy w zakresie używania db
#- dodać możliwość przeglądania statystyk dla każdego usera:
#       -dodatkowa tabela z datą i listą poprawnych/niepoprawnych odpowiedzi: data, login, fiszka, poprawne/niepoprawne
#       -możliwość podsumowania: ilość poprawnych/ niepoprawnych odpowiedzi, najczęściej/najrzadziej trenowana fiszka, ilość dni treningu