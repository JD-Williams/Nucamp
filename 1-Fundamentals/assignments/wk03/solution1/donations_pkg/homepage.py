#========================= 
# TASK 2
#=========================
def show_homepage():
    header_length = 30
    print()
    print(f" {'DonateMe Homepage'} ".center(header_length, '='))
    menu_options = ["Login","Register","Donate","Show Donations","Exit"]
    for idx, option in enumerate(menu_options):
        print(f"{'-'*(header_length)}".center(header_length))
        print(f"| {idx+1}.  {option.center(header_length-12)}     |")
    print(f"{'-'*(header_length)}".center(header_length))


#========================= 
# TASK 6
#=========================
def donate(username):
    is_valid = False
    while not is_valid:  # <- Bonus Task 4
        donation_amt = input("Enter amount to donate: ")
        is_valid = donation_amt.isdigit() and float(donation_amt) > 0
        if is_valid:
            break
        else:
            print("You must enter a positive number as the donation amount. Please try again.\n")
    donation_amt = float(donation_amt)
    donation = (username, donation_amt)  # <- Bonus Task 3
    print("Thank you for your donation!")
    return donation


#========================= 
# TASK 7
#=========================
def show_donations(donations):
    header_length = 50
    print()
    print(f" {'All Donations'} ".center(header_length, '-'))
    print()
    if donations:  # <- Bonus Task 3
        total_donations = 0
        for donation in donations:
            print(f"{donation[0]} donated ${donation[1]:.2f}.")
            total_donations += donation[1]
        print(f"\nTOTAL = ${total_donations:.2f}")
    else:
        print("Currently, there are no donations.")
    print()
