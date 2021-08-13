import random
import sys


#========================= 
# TASK 1
#=========================

heroes = {  # <-- Refactor code to transform into class objects
    '1': {
        'name': "Wizard",
        'hp': 70,
        'damage': 150,
    },
    '2': {
        'name': "Elf",
        'hp': 100,
        'damage': 100,
    },
    '3': {
        'name': "Human",
        'hp': 150,
        'damage': 20,
    },
    '4': {  # <-- Bonus Task 3
        'name': "Orc",
        'hp': 90,
        'damage': 110,
    }
}


#========================= 
# TASKS 2 & 3
#=========================

def displayOptions(options):
    for key, obj in options.items():
        print(f"{key})  {obj['name']}")

def displayDetails(id):
    print(f"The stats for your selected character are shown below:")
    for prop, value in heroes[id].items():
        print(f"{prop.title()}: {value}")
    print()

def selectCharacter():
    isValid = False
    while(not isValid):
        displayOptions(heroes)
        hero_names = [hero['name'].lower() for hero in heroes.values()]
        choice = input("Choose your character (or enter `Q` to quit): ").lower()
        print()
        if not (choice in heroes.keys() or choice in hero_names):  # <-- Bonus Tasks 1 & 2
            if choice == "q":  # <-- Bonus Task 4
                print("You have selected to `QUIT`. Thanks for using the app!")
                sys.exit(0)
            else:
                print(f"Unknown character. Try again.\n")
        else:
            if len(choice) > 1:
                choice = str(hero_names.index(choice)+1)
            isValid = True
    displayDetails(choice)
    return heroes[choice]


#========================= 
# TASK 4
#=========================

def strikes(attacker,defender):
    """
    Determines the outcome when an attacker attempts
    to strike a defender, and updates defender `hp`

    (dict,dict) -> int
    """
    isSuccessful = random.choice([0,1])  # <-- randomly choose if attack hits or misses
    if isSuccessful:
        defender['hp'] -= attacker['damage']
        print(f"The {attacker['name']} damaged the {defender['name']}!")
        print(f"The {defender['name']}'s hitpoints are now {defender['hp']}!")
    else:
        print(f"The {attacker['name']} missed!")
    print()
    return defender['hp']

def startBattle(hero):
    villain = {
        'name':"Dragon",
        'hp':300,
        'damage':50,
    }
    while True:
        villain['hp'] = strikes(hero,villain)  # <-- updates villain hp from strike
        if villain['hp'] <= 0:
            print(f"The {villain['name']} has lost the battle.")
            break

        hero['hp'] = strikes(villain,hero)    # <-- updates hero hp from strike
        if hero['hp'] <= 0:
            print(f"The {hero['name']} has lost the battle.")
            break


#========================= 
# AESTHETICS
#=========================

def titleScreen():
    print(r"""
/*========*\
|   THE    |
|  MENACE  |
|    OF    |
|  MORDOR  |
\*========*/
""")


#========================= 
# APPLICATION
#=========================

def replayGame():
    repeat = ['n','y']
    while True:
        option = input("Would you like to play again? (y/n): ").lower()
        if option in repeat:
            break
    return repeat.index(option)
    
def playGame():
    isRunning = 1
    while isRunning:
        titleScreen()
        character = selectCharacter()
        hero = character.copy()
        startBattle(hero)
        print()
        isRunning = replayGame()
        print()
    print("Thanks for using the app!")

playGame()
