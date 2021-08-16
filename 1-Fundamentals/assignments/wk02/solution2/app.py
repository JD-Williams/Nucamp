import sys
from textwrap import fill
from banking_pkg.account import User  # <-- Task 4


#========================= 
# TASK 2
#=========================
def create_username():
    is_valid = False
    while not is_valid:
        username = input("Enter a name to register: ")
        if 1 <= len(username) <= 10 and username.isalpha():  # <-- Bonus Task 1
            is_valid = True
        else:
            print("The username must consist of 1-10 letters. Please try again.")
            print()
    return username

def create_pin(username):
    is_valid = False
    while not is_valid:
        pin = input("Enter a pin: ")
        if len(pin) == 4 and pin.isdigit():  # <-- Bonus Task 2
            is_valid = True
        elif pin in username:
            print("The username must not contain your pin. Please try again")
        else:
            print("The PIN must contain exactly four digits. Please try again.")
    print()
    return pin

def user_exists(users, username, pin):
    for user in users:
        if user.username == username and user.pin == pin:
            return True
    return False

def register(users):  # <-- Main Menu: New Registration (Option 1)
    while True:
        new_username = create_username()
        new_pin = create_pin(new_username)
        if not user_exists(users, new_username, new_pin):
            new_user = User(new_username,new_pin)
            users.append(new_user)
            print(f"{new_user.username} has been registered with a starting balance of ${new_user.balance:.2f}.")
            return None
        else:
            print("A user with these credentials already exists in the system.")
            choice = input("Do you want to try again? (y/n) ").lower()
            if choice == 'y':
                print()
                continue
            elif choice == 'n':
                print("Please login with an existing set of credentials.")
                break
            else:
                print("Invalid entry!")
                break
    return None


#========================= 
# TASK 3
#=========================
def get_username():
    username = input("Enter name: ")
    return username

def get_pin():
    pin = input("Enter PIN: ")
    return pin

def login(users):  # <-- Main Menu: User Login (Option 2)
    max_errors = 3
    errors = 0
    while True:
        print("user login".upper())
        u = get_username()
        p = get_pin()
        for user in users:
            if user.username == u and user.pin == p:
                print("Login successful!\n")
                return user
        print("Invalid credentials!\n")
        errors += 1
        if errors >= max_errors:
            print(f"You had {errors} unsuccessful login attempts.") 
            choice = input(fill("Enter `Q` to quit to the main menu, otherwise hit any other key to continue: "))
            print()
            if choice.lower() == "q":
                return None


#========================= 
# TASK 4
#=========================

"""
See `account.py`
"""

#========================= 
# TASK 5
#=========================
def exit_app(*args):  # <-- Main Menu: Exit Application (Option 3)
    print("Thank you for using this ATM service.")
    sys.exit(0)

def get_option(obj_dict):
    options = obj_dict.keys()
    while True:
        option = input("Select a menu option: ")
        if not option in options:
            print("You entered an invalid option. Try again.\n")
        else:
            return option

def show_menu(menu_dict,user_obj=None):
    """
    Displays formatted options for each item in `menu_dict`.
    A custom username is shown if `userObj != None`.
    """
    header_length = 50
    print()
    print(f" {'automated teller machine'.upper()} ".center(header_length, '='))
    if user_obj !=None:
        print(f"User: {user_obj.username}")
    else:
        print()
    for k,obj in menu_dict.items():
        print(f"{'-'*(header_length)}".center(header_length))
        print(f"| {k}.  {obj['label'].center(header_length-12)}     |")
        print(f"{'-'*(header_length)}".center(header_length))

def atm():
    users = []
    active_user = None
    while not active_user:
        main_menu = {
            '1':{'label':"New Registration",'action':register},
            '2':{'label':"User Login",'action':login},
            '3':{'label':"Exit Application",'action':exit_app},
        }
        show_menu(main_menu,active_user)
        m_option = get_option(main_menu)
        if not users and m_option == "2":  # <-- prevents `login` action if no users are registered
            print()
            print(fill("Currently there are no users enrolled in the system. Please `Register` or `Exit` the application.\n"))
        else:
            print(f"You have selected `{main_menu[m_option]['label']}`\n")
            active_user = main_menu[m_option]['action'](users)  # <-- callback function from `main_menu`
            print()
            while active_user:  # <-- will execute only when a user is logged in
                user_menu = {
                    '1':{'label':"View Balance", 'action':active_user.show_balance},
                    '2':{'label':"Deposit Funds", 'action':active_user.deposit},
                    '3':{'label':"Withdraw Funds", 'action':active_user.withdraw},
                    '4':{'label':"Logout", 'action':active_user.logout},
                }
                show_menu(user_menu,active_user)
                u_option = get_option(user_menu)
                print(f"You have chosen to `{user_menu[u_option]['label']}`\n")
                active_user = user_menu[u_option]['action']()  # <-- calls the selected `User` object method

atm()
