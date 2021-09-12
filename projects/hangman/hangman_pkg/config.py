#========================================
# DISPLAY FUNCTIONS
#========================================

# Section title for CLI
def show_title(text):
    """Displays the text string with a variable-length border"""
    length = len(text) + 2
    title = [f"/*{'='*length}",f"| {text.upper()} |",f"{'='*length}*/"]
    for i in title:
        print(i)

# Title screen for CLI
def title_screen():
    """Displays a graphic in the command line"""
    CORPSE = (
      r'\ O /',
      r' \|/ ',
      r'  |  ',
      r' / \ ',
      '/   \\')
    screen = [
        f"/*{'='*22}*\\",
        f"|  {'hangman'.upper().ljust(15)}{CORPSE[0]}  |",
        f"|  {'for the CLI'.ljust(15)}{CORPSE[1]}  |",
        f"|  {' '.ljust(15)}{CORPSE[2]}  |",
        f"|  {'Made by:'.ljust(15)}{CORPSE[3]}  |",
        f"|  {'J.D.'.ljust(15)}{CORPSE[4]}  |",
        f"\\*{'='*22}*/",
    ]
    for i in screen:
        print(i)
    print()


#========================================
# HANDLER & VALIDATION FUNCTIONS
#========================================

def is_option_valid(obj_id, obj_list):
    """Validates that a user's selection is in a list.

    Parameters
    ----------
    obj_id : str
        A string id for a class instance.
    obj_list : list
        A list of instances for the same class.

    Returns
    -------
    bool
        True if successful, False otherwise.
    """
    err_msg = f"The selected option ({obj_id}) is invalid. Try again."
    try:
        int(obj_id)
    except ValueError:
        print(err_msg)
        return False
    else:
        if int(obj_id)-1 in range(len(obj_list)):
            return True
        else:
            print(err_msg)
            return False

def get_selection(obj_list):
    """Prompts user for input and returns the corresponding class instance.

    Parameters
    ----------
    obj_list : list
        A list of instances for the same class.

    Returns
    -------
    obj
        An instance of a class.
    """
    is_valid = False
    while not is_valid:
        obj_id = input("Enter a number for the desired option: ").lower()
        is_valid = is_option_valid(obj_id, obj_list)
    obj_id = int(obj_id)
    obj = obj_list[obj_id-1]
    return obj

def show_options(obj_list):
    """Display the name of each object in a list.
    
    Parameters
    ----------
    obj_list : list
        A list of instances for the same class.

    Returns
    -------
    None
    """
    for idx, obj in enumerate(obj_list):
        print(f"{idx+1} -- {str(obj.name).upper()} ({str(obj.label).title()})")

def get_menu_options(menu):
    """Prompts user to select a menu option from a list, and returns the corresponding 'Option' object.

    Parameters
    ----------
    menu : list
        A list of instances for the same class.

    Returns
    -------
    obj
        An instance of a class.
    """
    show_options(menu)
    obj = get_selection(menu)
    print()
    print(f"You have chosen to `{obj.label}`")
    return obj



if __name__ == '__main__':
    pass
