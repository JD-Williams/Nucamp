# OOP Banking Application in Python
#
# This demo script simulates the banking operations of 
# class-defined users to perform standard transactions
# on his/her account as well as other user accounts.
#

import time
from textwrap import fill

class User:
    """
    A class to represent a user
    
    ...

    Attributes
    ----------
    name : str
        A name assigned to a user instance that
        is 2-10 characters in length with no
        whitespace
    pin : int
        A 4-digit PIN for a user
    password : str
        A custom password for a user that is
        at least 5 characters in length


    Class Variables
    ---------------
    users : list
        A list of all `User` instances

    """
    users = []

    def __init__(self, name:str, pin:int, password:str):
        self.name = name
        self.pin = str(pin).zfill(4)
        self.password = password
        User.users.append(self)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):  # a string representation of the `User` instance for debugging
        kwarg_str = ", ".join(f"{attr}='{val}'" for attr, val in self.__dict__.items())
        return f"{self.__class__.__name__}({kwarg_str})"
    
    @staticmethod
    def is_str_valid(string, min_char=1, max_char=None):  # <-- Bonus Task 3
        if min_char and max_char:
            return (min_char <= len(string) <= max_char) and " " not in string
        elif min_char or max_char:
            return (
                (min_char <= len(string) and " " not in string) # string must be longer than min_char
                if min_char 
                else (len(string) <= max_char and " " not in string)) # string must be less than max_char
        else:
            return " " not in string

    @staticmethod
    def is_pin_valid(pin):  # <-- Bonus Task 3
        return pin.isdigit() and len(pin) == 4

    def get_name(self, *arg):
        min_char, max_char = 2, 10
        name = input(f"Enter a username: ")
        if self.is_str_valid(name, min_char, max_char):
            return name
        else:
            print(f"Invalid! A username must contain {min_char}-{max_char} characters with no spaces.\n")
            return None

    def get_pin(self, *arg):
        usr_name = arg[0] if arg else None
        pin = input(f"Enter {'your PIN' if not usr_name else 'a PIN for '+str(usr_name)}: ")
        if self.is_pin_valid(pin):
            return pin
        else:
            print("Invalid! A PIN must be exactly four digits.\n")
            return None

    def get_password(self):
        min_char = 5
        password = input(f"Enter your password: ")
        if self.is_str_valid(password, min_char):
            return password
        else:
            print(f"Invalid! A password must contain a least {min_char} characters with no spaces.\n")
            return None

    def change_name(self):
        new_name = self.get_name()
        if new_name and new_name.lower() != self.name.lower():
            self.name = new_name

    def change_pin(self):
        new_pin = self.get_pin()
        if new_pin and new_pin != self.pin:
            self.pin = new_pin

    def change_password(self):
        new_password = self.get_password()
        if new_password and new_password != self.password:
            self.password = new_password


class BankUser(User):
    """
    A class to represent a bank user
    
    ...

    Attributes
    ----------
    name : str
        A name assigned to a user instance that
        is 2-10 characters in length with no
        whitespace
    pin : int
        A 4-digit PIN for a user
    password : str
        A custom password for a user that is
        at least 5 characters in length
    balance : int
        The account balance for a `BankUser`
    on_hold : bool
        An attribute that indicates whether or
        not a hold is place on the account


    Class Variables
    ---------------
    bank_users : list
        A list of all `BankUser` instances
    acct_hold_msg : str
        A message displayed to a `BankUser` when a
        transaction is blocked due to an account hold
        (on_hold == True)

    """
    bank_users = []
    acct_hold_msg = fill("Unable to process this transaction due to an account hold. Please contact an administrator to resolve this matter.\n\n", width=50)

    def __init__(self, name, pin, password, balance=0, on_hold=False):
        super().__init__(name, pin, password)
        self.name = name
        self.pin = str(pin).zfill(4)
        self.password = password
        self.balance = balance
        self.on_hold = on_hold
        BankUser.bank_users.append(self)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):  # a string representation of the `BankUser` instance for debugging
        kwarg_str = ", ".join(f"{attr}='{val}'" for attr, val in self.__dict__.items())
        return f"{self.__class__.__name__}({kwarg_str})"

    def show_balance(self):
        print(f"{self.name} has an account balance of: ${self.balance:.2f}\n")

    def toggle_hold(self):  # <-- Bonus Task 5
        self.on_hold = not self.on_hold

    @staticmethod
    def is_amt_valid(amount, max_val=None):  # <-- Bonus Task 1 & 2
        try:
            float(amount)
        except ValueError:
            print("This is not a number.")
            return False
        else:
            if max_val:
                return 0 < float(amount) <= max_val
            return 0 < float(amount)

    def withdraw(self):
        if self.on_hold:  # <-- Bonus Task 5
            print(BankUser.acct_hold_msg)
            return
        amount = input("Enter an positive withdrawl amount: ")
        if self.is_amt_valid(amount, self.balance) and float(amount) <= self.balance:
            self.balance -= float(amount)
        elif float(amount) > self.balance:
            print("Operation cancelled! Insufficent funds.")
        else:
            print("Operation cancelled! Invalid amount.")

    def deposit(self):
        if self.on_hold:  # <-- Bonus Task 5
            print(BankUser.acct_hold_msg)
            return
        amount = input("Enter an positive deposit amount: ")
        if self.is_amt_valid(amount):
            self.balance += float(amount)
        else:
            print("Operation cancelled! Invalid amount.")

    @classmethod
    def get_user(cls):
        name = input("Enter the user's name: ")
        for user in BankUser.bank_users:
            if user.name.lower() == name.lower():
                return user
        return None

    def transfer_money(self):
        user = self.get_user()
        if not user:
            print("Operation cancelled! User does not exist.\n")
            return False
        elif self.on_hold or user.on_hold:  # <-- Bonus Task 5
            print(BankUser.acct_hold_msg)
            return False
        amount = input(f"Enter an amount to transfer to {user.name}: ")
        if not self.is_amt_valid(amount, self.balance):
            print("Operation cancelled! Amount invalid.\n")
            return False
        print(f"You are transferring ${float(amount):.2f} to {user.name}")
        print("Authentication required")
        pin = self.get_pin()
        if self.pin == pin:
            self.balance -= float(amount)
            user.balance += float(amount)
            print("Transfer authorized")
            print(f"Transferring ${float(amount):.2f} to {user.name}")
        else:
            print("Invalid PIN. Transaction canceled.")
        print(f"{self.name} has an account balance of ${self.balance:.2f}")
        print(f"{user.name} has an account balance of ${user.balance:.2f}\n")
        return self.pin == pin

    def request_money(self):
        user = self.get_user()
        if not user:
            print("Operation cancelled! User does not exist.\n")
            return False
        elif self.on_hold or user.on_hold:  # <-- Bonus Task 5
            print(BankUser.acct_hold_msg)
            return False
        amount = input(f"Enter an amount to request from {user.name}: ")
        if not self.is_amt_valid(amount, user.balance):
            print("Operation cancelled! Amount invalid.\n")
            return False
        elif float(amount) > user.balance:
            print(f"{user.name} has insufficent funds to complete this transaction.")
            return False
        print(f"You are requesting ${float(amount):.2f} from {user.name}")
        print("User authentication required...")
        pin = self.get_pin(user.name)
        if user.pin != pin:
            print("Invalid PIN. Transaction canceled.")
        else:
            print("Your password is required to complete this transaction.")
            password = self.get_password()
            if self.password == password:
                user.balance -= float(amount)
                self.balance += float(amount)
                print("Request authorized")
                print(f"{user.name} sent ${float(amount):.2f}")
            else:
                print("Invalid password! Transaction canceled.")
        print(f"{self.name} has an account balance of ${self.balance:.2f}")
        print(f"{user.name} has an account balance of ${user.balance:.2f}")
        return user.pin == pin and self.password == password


""" Driver Code for Task 1 """
def driver_code1():
    bob = User("Bob", 1234, "password")
    print(" ".join(str(v) for v in bob.__dict__.values()))
    User.users.clear()


""" Driver Code for Task 2 """
def driver_code2():
    bob = User("Bob", 1234, "password")
    bob.change_name()
    bob.change_pin()
    bob.change_password()
    print(" ".join(str(v) for v in bob.__dict__.values()))
    User.users.clear()


""" Driver Code for Task 3 """
def driver_code3():
    bob = BankUser("Bob", 1234, "password")
    print(" ".join(str(v) for v in bob.__dict__.values()))
    BankUser.bank_users.clear()


""" Driver Code for Task 4 """
def driver_code4():
    bob = BankUser("Bob", 1234, "password")
    bob.show_balance()
    bob.deposit()  # deposit $1000
    bob.show_balance()
    bob.withdraw()  # withdraw $500
    bob.show_balance()
    BankUser.bank_users.clear()


""" Driver Code for Task 5 """
def driver_code5():
    bob = BankUser("Bob", 1234, "password")
    alice = BankUser("Alice", 5678, "alicepassword")
    alice.deposit()  # deposit $5000
    alice.show_balance()
    bob.show_balance()
    alice.transfer_money()  # trf $500 to Bob
    alice.request_money()  # request $250 from Bob
    BankUser.bank_users.clear()


""" Driver Code for Bonus Task 5 """
def bonus5():
    bob = BankUser("Bob", 1234, "password")
    alice = BankUser("Alice", 5678, "alicepassword")
    karen = BankUser("Karen", int('0505'), "karenated")
    ken = BankUser("Ken", int('0704'), "YesIKen")
    
    # Make a deposit for Alice and transfer to Bob
    alice.show_balance()
    print("Deposit Funds".upper())
    alice.deposit()  # deposit $5000
    alice.show_balance()
    print("Transfer Funds".upper())
    alice.transfer_money()  # trf $1000 to Bob
    print("<--*-->\n\n")
    time.sleep(2)

    # Place a hold on Karen and block deposit
    karen.show_balance()
    karen.toggle_hold()
    print(f"{karen.name}'s account is {'on' if karen.on_hold else 'not on'} hold.\n")
    print("Deposit Funds".upper())
    karen.deposit()
    karen.show_balance()
    print("<--*-->\n\n")
    time.sleep(2)

    # Maintain hold on Karen and block funds request
    bob.show_balance()
    karen.show_balance()
    print(f"{karen.name}'s account is {'on' if karen.on_hold else 'not on'} hold.\n")
    print("Request Funds".upper())
    karen.request_money()   # request from Bob
    karen.show_balance()
    print("<--*-->\n\n")
    time.sleep(2)

    # Place a hold on Ken and block funds transfer
    ken.show_balance()
    ken.toggle_hold()
    print(f"{ken.name}'s account is {'on' if ken.on_hold else 'not on'} hold.\n")
    bob.show_balance()
    print("Transfer Funds".upper())
    bob.transfer_money()    # trf to $250 to Ken
    print("<--*-->\n\n")
    time.sleep(2)

    # Remove hold from Ken and allow funds transfer
    ken.show_balance()
    ken.toggle_hold()
    print(f"{ken.name}'s account is {'on' if ken.on_hold else 'not on'} hold.\n")
    bob.show_balance()
    print("Transfer Funds".upper())
    bob.transfer_money()    # trf to $250 to Ken
    print("<--*-->\n\n")
    
    BankUser.bank_users.clear()


""" Driver Code for All Tasks and Bonuses """
def run_tests():
    driver_code = [
        dict(label="Task 1", action=driver_code1),
        dict(label="Task 2", action=driver_code2),
        dict(label="Task 3", action=driver_code3),
        dict(label="Task 4", action=driver_code4),
        dict(label="Task 5", action=driver_code5),
        dict(label="Bonus Task 5", action=bonus5),
    ]
    for code in driver_code:
        border_length = 50
        header_txt = f"Driver Code for {code['label']}".center(border_length)
        print(f"{'='*border_length}")
        print(f"{header_txt}".upper().center(border_length))
        print("\nStarting...\n")
        code['action']()
        print("\n... Finished\n\n")
        time.sleep(5)



if __name__ == '__main__':
    run_tests()
