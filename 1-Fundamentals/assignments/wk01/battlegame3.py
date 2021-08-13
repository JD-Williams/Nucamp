import random
import sys

#========================= 
# TASK 1
#=========================
class Character():
    def __init__(self,name:str,hp:int,damage:int,**kwargs):
        self.name = name
        self.hp = hp
        self.damage = damage

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Character `{self.name}` (HP: {self.hp}, Damage: {self.damage})>"

    def details(self):
        max_length = max([len(attr) for attr in vars(self).keys()])
        for attr, val in vars(self).items():
            print(f"{attr.upper().ljust(max_length)} : {val}")
        print()

    def attacks(self,obj,hp,dmg):
        isSuccessful = random.choice([0,1])
        if isSuccessful:
            hp -= dmg
            print(f"The {self.name} damaged the {obj.name}!")
            print(f"The {obj.name}'s hitpoints are now {hp}!")
        else:
            print(f"The {self.name} missed!")
        print()
        return hp

    def battles(self,obj):
        attack_hp = self.hp
        attack_dmg = self.damage
        defend_hp = obj.hp
        defend_dmg = obj.damage
        while True:
            defend_hp = self.attacks(obj,defend_hp,attack_dmg)
            if defend_hp <= 0:
                print(f"The {obj.name} has lost the battle.")
                break
            attack_hp = obj.attacks(self,attack_hp,defend_dmg)
            if attack_hp <= 0:
                print(f"The {self.name} has lost the battle.")
                break

wizard = Character("Wizard",70,150)
elf = Character("Elf",100,100)
human = Character("Human",150,20)
orc = Character("Orc",90,110)  # <-- Bonus Task 3
dragon = Character("Dragon",300,50)

characters = []
heroes = [wizard,elf,human,orc]
villains = [dragon]


#========================= 
# TASKS 2 & 3
#=========================
def displayOptions(options):
    for obj in options:
        print(f"{options.index(obj)+1})  {obj.name}")

def getCharacter(options):
    isValid = False
    while not isValid:
        displayOptions(options)
        names = [obj.name.lower() for obj in options]
        choice = input("Choose your character (or enter `Q` to quit): ").lower()  # <-- Bonus Task 2
        print()
        if choice in names:  # <-- Bonus Task 1
            idx = names.index(choice)
            obj = options[idx]
            isValid = True
        elif choice.isdigit() and int(choice)-1 in range(len(options)):
            idx = int(choice) - 1
            obj = options[idx]
            isValid = True
        elif choice == "q":  # <-- Bonus Task 4
            print("You have selected to `QUIT`. Thanks for using the app!")
            sys.exit(0)
        else:
            print("Unknown character. Try again.\n")
    return obj
        

#========================= 
# TASK 4
#=========================
def playGame():
    isRunning = 1
    while isRunning:
        titleScreen()
        hero = getCharacter(heroes)
        villain = random.choice(villains)
        createBanner(hero,villain)  # <-- Can be replaced with `details` class method for each object
        print()
        hero.battles(villain)
        print()
        isRunning = replayGame()
        print()
    print("Thanks for using the app!")


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

def createBanner(hero,villain):
    hk_max = max([len(k) for k in vars(hero).keys()])
    hv_max = max([len(str(v)) for v in vars(hero).values()])
    vk_max = max([len(k) for k in vars(villain).keys()])
    vv_max = max([len(str(v)) for v in vars(hero).keys()])
    # Append attribute and value strings to respective lists
    h_keys, h_vals = [], []
    v_keys, v_vals = [], []
    for k, v in vars(hero).items():
        h_keys.append(f"{k.upper().ljust(hk_max)}")
        h_vals.append(f"{str(v).ljust(hv_max)}")
    for k, v in vars(villain).items():
        v_keys.append(f"{k.upper().ljust(vk_max)}")
        v_vals.append(f"{str(v).ljust(vv_max)}")
    # Display titles for hero and villain
    h_width = hk_max + hv_max + 3
    v_width = vk_max + vv_max + 3
    h_title = [f"/*{'='*6}*\\","|  HERO  |",f"\\*{'='*6}*/"]
    v_title = [f"/*{'='*9}*\\","|  VILLAIN  |",f"\\*{'='*9}*/"]
    for i in range(3):
        print(f"{h_title[i].center(h_width)}  |  {v_title[i].center(v_width)}")
    print(f"{''.ljust(h_width)}  |  {''.rjust(v_width)}")
    # Display details for hero and villain
    for i in range(len(h_keys)):
        print(f"{h_keys[i]} : {h_vals[i]}  |  {v_keys[i]} : {v_vals[i]}")


#========================= 
# APPLICATION
#=========================
def replayGame():
    repeat = ['n','y']
    attempts = 3
    while attempts:
        option = input("Would you like to play again? (y/n): ").lower()
        if option in repeat:
            break
        else:
            attempts -= 1
    if attempts == 0:
        return attempts
    return repeat.index(option)

playGame()
