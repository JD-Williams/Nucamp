#========================================
# DISPLAY FUNCTIONS
#========================================

# Section title for CLI
def show_title(text):
    length = len(text) + 2
    title = [f"/*{'='*length}",f"| {text.upper()} |",f"{'='*length}*/"]
    for i in title:
        print(i)

# Title screen for CLI
def title_screen():
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

def is_obj_valid(selection, obj_array):
    if selection.isdigit() and int(selection)-1 in range(len(obj_array)):
        idx = int(selection)-1
        return True, obj_array[idx]
    elif selection in [str(obj.name).lower() for obj in obj_array]:
        for obj in obj_array:
            if selection == str(obj.name).lower():
                return True, obj
    else:
        print(f"The selected option ({selection}) is invalid. Try again.")
        return False, None

def get_selection(obj_array):
    is_valid = False
    while not is_valid:
        selection = input("Select one of the options above: ").lower()
        is_valid, obj = is_obj_valid(selection, obj_array)
    return obj

def show_options(obj_array):
    for obj in obj_array:
        print(f"{obj_array.index(obj)+1} -- {str(obj.name).upper()} ({str(obj.label).title()})")

def get_menu_options(menu):
    show_options(menu)
    selection = get_selection(menu)
    print()
    print(f"You have chosen to `{selection.label}`")
    return selection

