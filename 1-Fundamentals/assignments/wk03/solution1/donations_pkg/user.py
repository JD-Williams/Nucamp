#========================= 
# TASK 4
#=========================
def login(database:dict):
    username = input("Enter a username: ").lower()
    password = input("Enter a password: ")
    print()
    if username in [u.lower() for u in database.keys()] and database[username] == password:  # <- Bonus Task 1
        print(f"Welcome back {username}!\n")
        return username
    elif username in [u.lower() for u in database.keys()] and database[username] != password:
        print(f"Incorrect password for `{username}`.\n")
        return ""
    else:
        print("User not found. Please register.\n")
        return ""


#========================= 
# TASK 5
#=========================
def register(database):
    while True:  # <- Bonus Task 2
        username = input("Enter a username: ").lower()
        if 0 < len(username) <= 10:
            break
        else:
            print("The username cannot be over 10 characters.\n")
    if username in [u.lower() for u in database.keys()]:  # <- Bonus Task 1
        print("Username already registered.\n")
        return ""
    while True:  # <- Bonus Task 2
        password = input("Enter a password: ")
        if len(password) >= 5:
            break
        else:
            print("The password must be at least 5 characters. Please try again.\n")
    print(f"Username {username} registered!\n")
    database[username] = password
    return username
