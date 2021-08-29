# A Backend Application for Collecting Donations made with Python
#
# This demo script simulates a text-based, fictional donations
# website called `DonateMe`.
#

from textwrap import fill
from donations_pkg.homepage import get_option, show_homepage, admin_settings, exit_app
from donations_pkg.user import Donation, User, Admin, login, register, logout


#========================= 
# TASK 3
#=========================
def donation_app():
    authorized_user = None
    while True:
        main_menu = {
            '1':{
                'label':"Login", 'action':login, 
                'login_required':False, 'admin_required':False},
            '2':{
                'label':"Register", 'action':register, 
                'login_required':False, 'admin_required':False},
            '3':{
                'label':"Show All Donations", 'action':Donation.show_donations, 
                'login_required':False, 'admin_required':False},
            '4':{
                'label':"Make Donation", 'action':authorized_user.donate if authorized_user else None,
                'login_required':True, 'admin_required':False},
            '5':{
                'label':"View My Donations", 'action':authorized_user.my_donations if authorized_user else None, 
                'login_required':True, 'admin_required':False},
            '6':{
                'label':"Logout", 'action':logout, 
                'login_required':True, 'admin_required':False},
            'S':{
                'label':"Administrative Settings", 'action':admin_settings, 
                'login_required':True, 'admin_required':True},
            'Q':{
                'label':"Exit", 'action':exit_app, 
                'login_required':False, 'admin_required':False},
        }
        show_homepage(main_menu, authorized_user)
        if authorized_user:
            print(f"Logged in as: {authorized_user.username}")
        else:
            print("You must login to make a donation or view your donations.")
        choice = get_option(main_menu)
        print()
        if main_menu[choice]['login_required'] == True and authorized_user == None:
            print(fill(f"You selected `{main_menu[choice]['label']}`, however, you must be logged in to access this feature. Please select another option.\n"))
            continue
        if main_menu[choice]['admin_required'] == True and authorized_user.is_admin == False:
            print(fill(f"You selected `{main_menu[choice]['label']}`, however, you must be an administrator to access this feature. Please select another option.\n"))
            continue
        authorized_user = main_menu[choice]['action'](authorized_user)


if __name__ == '__main__':
    donation_app()
