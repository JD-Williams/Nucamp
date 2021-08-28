import sys

#========================= 
# TASK 2
#=========================
def get_option(obj_dict:dict):
    options = [k.upper() for k in obj_dict.keys()]
    while True:
        option = input("Select a menu option: ").upper()
        if not option in options:
            print("You entered an invalid option. Try again.\n")
        else:
            return option

def show_menu(menu_options:dict, user=None, header_text="DonateMe Homepage"):
    header_length = 50
    print()
    print(f" {header_text} ".center(header_length, '='))
    for idx, option_obj in menu_options.items():
        if not user and option_obj['login_required']==True:
            continue
        if user and user.is_admin == False and option_obj['admin_required'] == True:
            continue
        print(f"{'-'*(header_length)}".center(header_length))
        print(f"| {idx}.  {option_obj['label'].center(header_length-12)}     |")
    print(f"{'-'*(header_length)}".center(header_length))

def show_homepage(menu_options, user=None):
    show_menu(menu_options, user)

def admin_settings(admin, *args):
    while True:
        admin_menu = {
            '1':{
                'label':"Change User Password", 'action':admin.change_password, 
                'login_required':True, 'admin_required':True},
            '2':{
                'label':'Change User Privileges', 'action':admin.change_privileges,
                'login_required':True, 'admin_required':True},
            'Q':{
                'label':"Return to Main Menu", 'action':None, 
                'login_required':True, 'admin_required':True},
        }
        show_menu(admin_menu, admin, "Administrative Settings")
        choice = get_option(admin_menu)
        print()
        if choice == "Q":
            return admin
        else:
            admin = admin_menu[choice]['action'](admin)

def exit_app(*args):
    print("Thank you for using this application. Have a great day!")
    sys.exit(0)
