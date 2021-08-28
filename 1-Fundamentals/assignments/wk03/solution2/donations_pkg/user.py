import uuid  # <-- required for primary key in database operations
from textwrap import fill
from datetime import datetime


class Donation:
    """
    A class to represent a donation.
    
    ...

    Attributes
    ----------
    value : float
        The amount of the donation
    donor : User.username
        The username of the person who donated
    created_at : datetime
        The timestamp of whenthe donation was made
    timestamp_str : str
        A string representation of the timestamp

    """
    donations = []

    def __init__(self, value, donor=None):
        self.uid = uuid.uuid4()
        self.value = float(value)
        self.donor = donor
        self.created_at = datetime.now()
        self.timestamp_str = datetime.strftime(self.created_at,'%Y-%m-%d %H:%M:%S')
        Donation.donations.append(self)

    def __str__(self):
        return f"<{self.__class__.__name__}: ${self.value:.2f} ({self.timestamp_str})>"

    def __repr__(self):
        return f"{self.__class__.__name__}(value='{self.value}')"

    #========================= 
    # TASK 7
    #=========================
    @classmethod
    def show_donations(cls, *args, show_all=True, header_text="All Donations"):
        """
        Displays each donation made by all users. If a `User` object is
        passed into the function as an optional argument, only
        donations made by the specified user will be displayed.
        """
        user = args[0] if args else None  # <-- a `User` object passed as an optional arg
        header_length = 50
        print()
        print(f" {header_text} ".center(header_length, '-'))
        print()
        if Donation.donations:  # <- Bonus Task 3
            total = 0
            for donation in user.donations if user != None and show_all == False else Donation.donations:
                print(f"{'You' if user != None and user.username == donation.donor else donation.donor} donated ${donation.value:.2f} (Timestamp: {donation.timestamp_str})")
                total += donation.value
            print(f"\nTOTAL = ${total:.2f}")
        else:
            print("Currently, there are no donations.")
        print()
        return user


class User:
    """
    A class to represent a user
    
    ...

    Attributes
    ----------
    uid : UUID object
        A unique identifier that can be used as
        a primary key in a database
    username : str
        A custom username for a user
    password : str
        A custom password for a user
    is_admin : bool = False
        A boolean that indicates whether a user
        has administrative privileges
    donations : list
        A list that contains all
        donations made by a user

    """
    users = []

    def __init__(self, username=None, password=None, is_admin=False):
        self.uid = uuid.uuid4()
        self.username = username
        self.password = password
        self.is_admin = is_admin
        self.donations = []
        if self.username:
            self.username.lower()
        User.users.append(self)

    def __str__(self):
        return f"<{self.__class__.__name__} `{self.username}`>"

    def __repr__(self):
        return f"{self.__class__.__name__}(username='{self.username}', password='{self.password}')"

    @staticmethod
    def is_amount_valid(amount):
        return amount.isdigit() and 0 < float(amount)

    #========================= 
    # TASK 6
    #=========================
    def donate(self, *args):
        is_valid = False
        while not is_valid:  # <- Bonus Task 4
            donation_amt = input("Enter amount to donate: ")
            is_valid = donation_amt.isdigit() and float(donation_amt) > 0
            if is_valid:
                break
            else:
                print("You must enter a positive number as the donation amount. Please try again.\n")
        new_donation = Donation(float(donation_amt), self.username)
        self.donations.append(new_donation)
        print("Thank you for your donation!")
        return self

    def my_donations(self, *args):
        Donation.show_donations(self, show_all=False, header_text="My Donations")
        return self


class Admin(User):
    """
    A subclass that represents a user
    with administrative privileges

    ...

    username : str
        A custom username for a user
    password : str
        A custom password for a user
    is_admin : bool = True
        A boolean that indicates whether a user
        has administrative privileges

    """
    def __init__(self, username=None, password=None):
        super().__init__(username, password)
        self.username = username
        self.password = password
        self.is_admin = True
        if self.username:
            self.username.lower()

    def __str__(self):
        return f"<{self.__class__.__name__} `{self.username}`>"

    def __repr__(self):
        return f"{self.__class__.__name__}(username='{self.username}', password='{self.password}')"

    def confirm_change(self):
        admin_password = input("Enter your administrative password to confirm the change: ")
        if admin_password != self.password:
            print("Invalid admin password! The transaction has been cancelled.\n")
        return admin_password == self.password

    def change_password(self, *args):  # <-- Admin Setting #1
        target = None
        username = set_username()
        for user in User.users:
            if username == user.username:
                target = user
                new_password = set_password()
                if self.confirm_change():
                    print(fill(f"The password for {target.username} was changed from `{target.password}` to `{new_password}`.\n"))
                    target.password = new_password
                return self
        print(f"There is no user named `{username}` in the system.\n")
        return self

    @staticmethod
    def promote_user(target):
        """
        This object method copies the attributes of an existing `User` instance to
        a new `Admin` instance, elevates administrative privileges (`is_admin=True`), 
        and removes the original `User` instance from the class variable `User.users`.
        """
        attrs = vars(target)
        new_admin = Admin()
        for k, v in attrs.items():
            setattr(new_admin, k, v)
        if hasattr(new_admin, "is_admin"):
            setattr(new_admin, "is_admin", True)
        User.users.pop(User.users.index(target))
        print(f"The user `{new_admin.username}` has been promoted to an admin.\n")

    @staticmethod
    def more_than_one_admin():
        num_of_admins = len(list(filter(lambda x: isinstance(x, Admin), User.users)))
        return num_of_admins > 1

    def demote_admin(self, target):
        """
        This object method copies the attributes of an existing `Admin` instance to
        a new `User` instance, revokes administrative privileges (`is_admin=False`), 
        and removes the original `Admin` instance from the class variable `User.users`.
        """
        if self.more_than_one_admin():
            attrs = vars(target)
            new_user = User()
            for k, v in attrs.items():
                setattr(new_user, k, v)
            if hasattr(new_user, "is_admin"):
                setattr(new_user, "is_admin", False)
            User.users.pop(User.users.index(target))
            print(f"The admin `{new_user.username}` has been demoted to an user.\n")
        else:
            print(fill("This transaction cannot be completed since there must be at least one admin in the system.\n"))

    def change_privileges(self, *args):  # <-- Admin Setting #2
        """
        This object method allows an admin (`is_admin=True`) to toggle the privileges for any
        `User` or `Admin` instance. 
        """
        target = None
        username = set_username()
        for user in User.users:
            if username == user.username:
                target = user
                if user.is_admin == True:
                    print(f"{target.username} will be changed from an admin to a standard user.")
                    if self.confirm_change():
                        self.demote_admin(target)
                else:
                    print(f"{target.username} will be changed from a standard user to an admin.")
                    if self.confirm_change():
                        self.promote_user(target)
                return self
        print(f"There is no user named `{username}` in the system.\n")
        return self

admin = Admin("admin","password123")


#========================= 
# TASK 4
#=========================
def login(*args):
    username = input("Enter a username: ").lower()
    password = input("Enter a password: ")
    print()
    for user in User.users:
        if username == user.username and password == user.password:  # <- Bonus Task 1
            print(f"Welcome back {username}!\n")
            return user
        elif username == user.username and password != user.password:
            print(f"Incorrect password for `{username}`.\n")
            return None
    print("User not found. Please register.\n")
    return None

#========================= 
# TASK 5
#=========================
def set_username():
    while True:  # <- Bonus Task 2
        username = input("Enter a username: ").lower()
        if 0 < len(username) <= 10:
            break
        else:
            print("The username cannot be over 10 characters.\n")
    return username

def set_password():  # <- Bonus Task 2
    while True:
        password = input("Enter a password: ")
        if len(password) >= 5:
            break
        else:
            print("The password must be at least 5 characters. Please try again.\n")
    return password

def does_user_exist(username):
    for user in User.users:
        if username == str(user.username).lower():  # <- Bonus Task 1
            print("Username already registered.\n")
            return True
    return False

def register(*args):
    active_user = args[0] if args else None
    username = set_username()
    if does_user_exist(username):
        return None
    password = set_password()
    print(f"Username {username} registered!\n")
    new_user = User(username, password)
    return new_user if active_user == None or active_user.is_admin == False else active_user

def logout(*args):
    print("You have successfully logged out.\n")
    return None
