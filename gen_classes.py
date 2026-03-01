from enum import IntEnum

class Choice(IntEnum):
    create_new_user = 1
    login_in_to_program = 2    
    add_flashcard = 3
    exit = 4

class ChoiceInner(IntEnum):
    change_settings = 1
    change_password = 2
    delete_user = 3
    learning = 4
    main_menu = 5
