from textwrap import fill


#========================= 
# TASK 4
#=========================
class Customer:

    customers = []

    def __init__(self, username, pin, balance:int=0):
        self.username = username
        self.pin = pin
        self.balance = balance
        Customer.customers.append(self)

    def __str__(self):
        return f"<Customer `{self.username}` (Balance: ${self.balance:.2f})>"

    def __repr__(self):
        return f"Customer(username='{self.username}', pin='{self.pin}')"

    def show_balance(self):
        print(f"Current Balance: ${self.balance:.2f}")
        return self

    @staticmethod
    def is_amount_valid(amount, max_amount=None):
        if max_amount == None:
            return amount.isdigit() and 0.00 < float(amount)
        return amount.isdigit() and 0.00 < float(amount) < max_amount

    def deposit(self):
        is_valid = False
        while not is_valid:
            amount = input("Enter a whole dollar amount to deposit: ")
            if self.is_amount_valid(amount):
                self.balance += float(amount)
                is_valid = True
                self.show_balance()
            else:
                print("The deposit amount is invalid. Please try again.")
        return self

    def withdraw(self):
        is_valid = False
        while not is_valid:
            amount = input("Enter a whole dollar amount to withdraw: ")
            if self.is_amount_valid(amount, self.balance):  # <-- Bonus Task 3
                self.balance -= float(amount)
                is_valid = True
                self.show_balance()
            else:
                print(fill(f"The requested withdrawl amount must be a positive value that does not exceed your current balance (${self.balance:.2f})."))
        return self

    def logout(self):
        print(f"Goodbye {self.username}!")
        return None
