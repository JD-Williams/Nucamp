#========================= 
# TASK 4
#=========================

def show_balance(balance):
    print(f"Current Balance: ${balance}")

def deposit(balance):
    amount = float(input("Enter amount to deposit: "))
    balance += amount
    return balance

def withdraw(balance):
    amount = float(input("Enter amount to withdraw: "))
    balance -= amount
    return balance

def logout(name):
    print(f"Goodbye {name}!")
