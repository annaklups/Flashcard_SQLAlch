import os

def directory_path(file_name):
    """Returning directory path for another file in the main program files's folder"""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)

def repeat_function(function, question, *args):
    """Simple function that repeats (or not) provided function based on user inputs"""
    answer = 'yes'
    while answer in ('yes', 'YES', 'Yes', 'y', 'Y'):
        if args:
            function(*args)
        else:
            function()
        while True:
            answer = input(question)
            if answer in ('yes', 'YES', 'Yes', 'y', 'Y'):
                break
            elif answer in ('no', 'NO', 'No', 'n', 'N'):
                break
            else:
                continue