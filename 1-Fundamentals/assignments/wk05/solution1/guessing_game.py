import random
import time
from textwrap import fill


class OutOfBoundsError(Exception):  # <- Bonus Task 1
    pass

#========================= 
# TASK 1
#=========================
def guess_random_number(tries, start, stop):
    rnd_num = random.randint(start, stop)
    guesses = []  # <- Bonus Task 3
    while tries:
        print(f"Number of tries left: {tries}")
        try:
            guess = int(input(f"Guess a number between {start} and {stop}: "))
            if not start <= guess <= stop:
                raise OutOfBoundsError
        except ValueError:
            print("This is not a number. Try again.\n")
        except OutOfBoundsError:  # <- Bonus Task 1
            print("Your guess is out of range.")
        else:
            if guess in guesses:  # <- Bonus Task 3
                print("You already guessed this number.")
                continue
            elif guess == rnd_num:
                print("You guessed the correct number!")
                return True
            else:
                print(f"Guess {'higher' if guess < rnd_num else 'lower'}!")
                guesses.append(guess)  # <- Bonus Task 3
                tries -= 1
    if not tries:
        print(f"Tough luck! The correct number was {rnd_num}.")
        return False


#========================= 
# TASK 2
#=========================
def guess_random_num_linear(tries, start, stop):
    rnd_num = random.randint(start, stop)
    print(f"The number for the program to guess is {rnd_num}")
    for guess in range(start, stop+1):
        print(f"Number of tries left: {tries}")
        tries -= 1
        print(f"The program is guessing... {guess}")
        if guess == rnd_num:
            print("The program has guessed the correct number!\n")
            return True
        if tries == 0:
            print("The program failed to guess the correct number.\n")
            return False

#========================= 
# TASK 3
#=========================
def guess_random_num_binary(tries, start, stop):
    rnd_num = random.randint(start, stop)
    print(f"Random number to find: {rnd_num}")
    potentials = list(range(start, stop+1))
    lo = 0
    hi = len(potentials) - 1
    while lo <= hi:
        pivot = (lo + hi) // 2
        pivot_value = potentials[pivot]
        if pivot_value == rnd_num:
            print(f"Found it! {rnd_num}\n")
            return True
        else:
            if not tries:
                break
            if pivot_value > rnd_num:
                print("Guessing lower!")
                hi = pivot - 1
            else:
                print("Guessing higher!")
                lo = pivot + 1
        tries -= 1
    print("Your program failed to find the number.\n")
    return False


# Bonus Task 2
def show_guess_methods(dict_obj):
    print("random number guess methods".upper())
    for k,v in dict_obj.items():
        print(f"{k} - {v['label']}")

def is_option_valid(choice, list_obj):
    if not choice in list_obj:
        print("You selected an invalid option. Try again.\n")
    return choice in list_obj

def get_parameter(name:str, *args):
    lower_bound = args[0] if args else None
    while True:
        try:
            value = int(input(f"Enter the {name}: "))
        except ValueError:
            print("This is not a number.")
        else:
            if lower_bound != None and lower_bound >= value:
                print(f"The upper bound must be greater than the lower bound ({lower_bound}).")
                continue
            elif not 0 <= value:
                print("This is not a positive integer.")
                continue
            else:
                return value

def select_guess_method():
    options = {
        '1': dict(label="User Input", action=guess_random_number),
        '2': dict(label="Linear Search", action=guess_random_num_linear),
        '3': dict(label="Binary Search", action=guess_random_num_binary),
    }
    tries = get_parameter("number of tries")
    start = get_parameter("lower bound of the guess interval")
    stop = get_parameter("upper bound of the guess interval", start)
    print()
    show_guess_methods(options)
    while True:
        option = input(fill("Select the corresponding number of the desired guess method for the options listed: "))
        if is_option_valid(option, options.keys()):
            break
    print(f"\nYou chose '{options[option]['label']}' as your guess method.\n")
    options[option]['action'](tries, start, stop)
    print()


# Bonus Task 4
class Player:
    """
    A class to represent a player
    
    ...

    Attributes
    ----------
    winnings : int
        The value of a player's total winnings
        after a bet is placed and executed


    Class Variables
    ---------------
    TEXT_WIDTH : int
        Represents the maximum character length
        of all messages output to the player

    """
    TEXT_WIDTH = 50

    def __init__(self, winnings:int=10):
        self.winnings = winnings

    def get_bet(self):
        try:
            wager = int(input(f"Enter a whole dollar amount to wager up to ${self.winnings if self.winnings < 10 else 10}: "))
        except ValueError:
            print("This is not an integer.")
        else:
            if not 0 < wager <= min(self.winnings, 10):
                print(f"You cannot bet $0 or less, nor more than ${min(self.winnings, 10)}.")
                return None
            return wager

    def get_outcome(self):
        choices = ['n', 'y']
        choice = input(fill("Do you think the computer will guess the correct number? (y/n): ", width=self.TEXT_WIDTH)).lower()
        if choice[0] not in ['n', 'y']:
            print("Invalid selection. Please choose 'y' or 'n'.")
            return None
        return choices.index(choice[0])

    def gamble(self, func=guess_random_num_linear):
        rounds = 0
        while 0 < self.winnings < 50:
            rounds += 1
            print(f"round {str(rounds).zfill(2)}".upper())
            print(fill("The computer will guess a random number using a 'Linear Search' algorithm.", width=self.TEXT_WIDTH))
            while True:
                prediction = self.get_outcome()
                if prediction: break
            while True:
                bet = self.get_bet()
                if bet: break
            tries = random.randint(5, 5) 
            start = random.choice(range(1,101))
            stop = start + (2*tries)
            is_computer_successful = func(tries, start, stop)
            if prediction == is_computer_successful:
                self.winnings += bet*2
            else:
                self.winnings -= bet
            print(f"Total Winnings: ${self.winnings}\n\n")
        if self.winnings >= 50:
            print(f"Congratulations! You played {rounds} rounds and earned a total of ${self.winnings}.")
        else:
            print(f"Tough luck. You played {rounds} {'rounds' if rounds > 1 else 'round'}... and you have nothing to show for it.")


""" Driver Code for Task 1 """
def driver_code1():
    guess_random_number(5, 0, 10)

""" Driver Code for Task 2 """
def driver_code2():
    guess_random_num_linear(5, 0, 10)

""" Driver Code for Task 3 """
def driver_code3():
    guess_random_num_binary(5, 0, 100)

""" Driver Code for Bonus Task 2 """
def bonus2():
    select_guess_method()

""" Driver Code for Bonus Task 4 """
def bonus4():
    player1 = Player()
    player1.gamble()

""" Driver Code for All Tasks and Bonuses """
def run_tests():
    driver_code = [
        dict(label="Task 1", action=driver_code1),
        dict(label="Task 2", action=driver_code2),
        dict(label="Task 3", action=driver_code3),
        dict(label="Bonus Task 2", action=bonus2),
        dict(label="Bonus Task 4", action=bonus4),
    ]
    for code in driver_code:
        border_length = 50
        header_txt = f"Driver Code for {code['label']}".center(border_length)
        print(f"{'='*border_length}")
        print(f"{header_txt}".upper().center(border_length))
        print("\nStarting...\n")
        code['action']()
        print("\n... Finished\n\n")
        time.sleep(3)



if __name__ == '__main__':
    run_tests()
