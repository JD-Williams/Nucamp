#========================= 
# TASK 1
#=========================

wizard = "Wizard"
elf = "Elf"
human = "Human"

hp_wizard = 70
hp_elf = 100
hp_human = 150

damage_wizard = 150
damage_elf = 100
damage_human = 20

hp_dragon = 300
damage_dragon = 50


#========================= 
# TASK 2
#=========================
"""
print("1)", wizard)
print("2)", elf)
print("3)", human)
choice = input("Choose your character: ")
"""

#========================= 
# TASK 3
#=========================

while(True):
    print("1)", wizard)
    print("2)", elf)
    print("3)", human)
    choice = input("Choose your character: ")
    if choice == "1":
        my_name = wizard
        my_hp = hp_wizard
        my_damage = damage_wizard
        break
    if choice == "2":
        my_name = elf
        my_hp = hp_elf
        my_damage = damage_elf
        break
    if choice == "3":
        my_name = human
        my_hp = hp_human
        my_damage = damage_human
        break
    print("Unknown character")
print(f"You have chosen the character: {my_name}")
print(f"Health: {my_hp}")
print(f"Damage: {my_damage}")
print()


#========================= 
# TASK 4
#=========================

while True:
    hp_dragon -= my_damage
    print(f"The {my_name} damaged the Dragon!")
    print(f"The Dragon's hitpoints are now: {hp_dragon}")
    print()
    if hp_dragon <= 0:
        print("The Dragon has lost the battle.")
        break

    my_hp -= damage_dragon
    print(f"The Dragon strikes back at {my_name}")
    print(f"The {my_name}'s hitpoints are now: {my_hp}")
    print()
    if my_hp <= 0:
        print(f"The {my_name} has lost the battle.")
        break
