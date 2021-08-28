import sys
from donations_pkg.homepage import show_homepage, donate, show_donations
from donations_pkg.user import login, register


database = {"admin": "password123"}
donations = []
authorized_user = ""

#========================= 
# TASK 3
#=========================
while True:
    show_homepage()
    if authorized_user == "":
        print("You must be logged in to donate")
    else:
        print(f"Logged in as: {authorized_user}")
    choice = input("Choose an option: ")
    print()
    if choice == "1":
        authorized_user = login(database)
    elif choice == "2":
        authorized_user = register(database)
    elif choice == "3":
        if authorized_user == "":
            print("You are not logged in.")
        else:
            donation = donate(authorized_user)
            donations.append(donation)
    elif choice == "4":
        show_donations(donations)
    elif choice == "5":
        print("Thank you for using this application. Have a great day!")
        sys.exit(0)
    else:
        print("Option invalid! Please try again.\n")
