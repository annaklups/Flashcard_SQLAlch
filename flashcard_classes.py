import sqlite3
import ast

from gen_functions import directory_path

class User:
    def __init__(self, login, password, flash_amount = 10, new_flash_amount = 5, user_num = None):
        if user_num == None:
            conn = sqlite3.connect(directory_path("flashcards_db.db"))
            c = conn.cursor()
            c.execute("SELECT MAX(user_num) FROM users_tab;")
            users_amount_db_max, = c.fetchall()[0]
            user_num = int(users_amount_db_max or 0) + 1
            conn.commit()
            conn.close()  
        
        self.login = login
        self.password = password
        self.flash_amount = flash_amount
        self.new_flash_amount = new_flash_amount
        self.user_num = user_num

    def __repr__(self):
        return f"User: {self.user_num}: {self.login}"

    def create_user(self):
        """Method to create new user in db"""
        conn = sqlite3.connect(directory_path("flashcards_db.db"))
        c = conn.cursor()
        c.execute("SELECT login FROM users_tab WHERE login = ?", (self.login,))
        is_in_db = c.fetchall()
        if not is_in_db:
            c.execute("INSERT INTO users_tab VALUES (?,?,?,?,?);", (self.user_num, self.login, self.password, self.flash_amount, self.new_flash_amount))
            c.execute("SELECT MAX(flash_num) FROM flashcards_tab;")
            flashcards_amount_db_max, = c.fetchall()[0]
            new_wages = dict.fromkeys(range(1, flashcards_amount_db_max+1), 5)
            c.execute("INSERT INTO users_info_tab VALUES (?,?);", (self.user_num, str(new_wages)))
            print(f"User {self.login} added to db")
        else:
            print(f"User {self.login} already exists in database")
        conn.commit()
        conn.close()
    
    def change_settings(self):
        """Method to change user's settings - number of flashcards shown to user"""
        conn = sqlite3.connect(directory_path("flashcards_db.db"))
        c = conn.cursor()
        c.execute("UPDATE users_tab SET flash_amount = ?, new_flash_amount = ? WHERE login = ?;", (self.flash_amount, self.new_flash_amount, self.login))
        conn.commit()
        conn.close()                
        return print("Settings changed correctly")

    def delete_user(self):
        """Method to delete the user from db"""
        conn = sqlite3.connect(directory_path("flashcards_db.db"))
        c = conn.cursor()
        c.execute("DELETE FROM users_tab WHERE login = ?;", (self.login,))
        c.execute("DELETE FROM users_info_tab WHERE user_num = ?;", (self.user_num,))
        conn.commit()
        conn.close()                
        return print("User was deleted from the database")

    def change_password(self):
        """Method to change the password for user"""
        conn = sqlite3.connect(directory_path("flashcards_db.db"))
        c = conn.cursor()
        c.execute("UPDATE users_tab SET password = ? WHERE login = ?;", (self.password, self.login))
        conn.commit()
        conn.close()                
        return print("Settings changed correctly")

class Flashcard:
    def __init__(self, pol, translate, topic, flash_num = None):
        if flash_num == None:
            conn = sqlite3.connect(directory_path("flashcards_db.db"))
            c = conn.cursor()
            c.execute("SELECT MAX(flash_num) FROM flashcards_tab;")
            flashcards_amount_db_max, = c.fetchall()[0]
            flash_num = int(flashcards_amount_db_max or 0) + 1
            conn.commit()
            conn.close()              
        
        self.flash_num = flash_num
        self.pol = pol
        self.translate = translate
        self.topic = topic
        self.flash_num = flash_num

    def __repr__(self):
        return f"Flashcard: {self.flash_num}: {self.pol} - {self.translate}"
    
    def add_1_flashcard_to_db(self):
        """Method to add to db one new flashcard. 
        Method updates wages of existing users by adding new flashcard number to their wages
        """
        conn = sqlite3.connect(directory_path("flashcards_db.db"))
        c = conn.cursor()
        c.execute("SELECT * FROM flashcards_tab WHERE pol = ?", (self.pol,))
        is_in_db = c.fetchall()
        if not is_in_db:
            c.execute("INSERT INTO flashcards_tab VALUES (?,?,?,?);", (self.flash_num, self.pol, self.translate, self.topic))
            print(f"Flashcard: {self.flash_num}: {self.pol} - {self.translate} added to database")
            c.execute("SELECT MAX(user_num) FROM users_tab;")
            users_amount_db_max, = c.fetchall()[0]
            if users_amount_db_max:
                for user_num in range(1, users_amount_db_max+1):
                    c.execute("SELECT wages FROM users_info_tab WHERE user_num = ?", (user_num,))
                    str_wages, = c.fetchall()[0]
                    wages = ast.literal_eval(str_wages)
                    wages[self.flash_num] = 5
                    c.execute("UPDATE users_info_tab SET wages = ? WHERE user_num = ?;", (str(wages), user_num))
        else:
            print(f"{self.pol} - {self.translate} already exists in database")
        conn.commit()
        conn.close()

    def learn_flashcard(self):
        """Method to show flashcard and check corectness of user's answer.
        Returns wage change for this flashcard: 1 for correct answer, -1 for incorrect answer.
        """
        print(f"Flashcard number:{self.flash_num} - POL: {self.pol.upper()}")
        answer = input("Please provide translation:")
        if answer.lower() == self.translate:
            print("Correct answer!!")
            return -1
        else:
            print(f"You have to work on that. Correct answer is: {self.translate}")
            return 1

