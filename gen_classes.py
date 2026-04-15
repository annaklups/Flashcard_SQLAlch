from enum import IntEnum

class Choice(IntEnum):
    """Class simplifying chosing options in main menu"""
    create_new_user = 1
    login_in_to_program = 2    
    add_flashcard = 3
    exit = 4

class ChoiceInner(IntEnum):
    """Class simplifying chosing options in inner menu"""
    change_settings = 1
    change_password = 2
    delete_user = 3
    learning = 4
    main_menu = 5
