from banking_pkg import account  # <-- Task 5

def atm_menu(name):
    print("")
    print("          === Automated Teller Machine ===          ")
    print("User: " + name)
    print("------------------------------------------")
    print("| 1.    Balance     | 2.    Deposit      |")
    print("------------------------------------------")
    print("------------------------------------------")
    print("| 3.    Withdraw    | 4.    Logout       |")
    print("------------------------------------------")


#========================= 
# TASK 2
#=========================

user = input("Enter name to register: ")
pin = input("Enter PIN: ")
balance = 0.00

print(f"{user} has been registered with a starting balance of ${balance}\n")


#========================= 
# TASK 3
#=========================

while True:
    print("          === Automated Teller Machine ===          ")
    print("LOGIN")
    name_to_validate = input("Enter name: ")
    pin_to_validate = input("Enter PIN: ")
    if name_to_validate == user and pin_to_validate == pin:
        print("Login successful!\n")
        break
    else:
        print("invalid credentials!\n")

"""
is_logged_in = True
while is_logged_in:
    atm_menu(user)
    option = input("Choose an option: ")
"""

#========================= 
# TASK 4
#=========================

"""
See `account.py`
"""

#========================= 
# TASK 5
#=========================

is_logged_in = True
while is_logged_in:
    atm_menu(user)
    option = input("Choose an option: ")
    if option == "1":
        account.show_balance(balance)
    elif option == "2":
        balance = account.deposit(balance)
        account.show_balance(balance)
    elif option == "3":
        balance = account.withdraw(balance)
        account.show_balance(balance)
    elif option == "4":
        account.logout(user)
        break
    else:
        print("Invalid selection! Try again.")

    