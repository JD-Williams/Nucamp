import random
import sys
from textwrap import fill, wrap
import time
import copy
# import speech_recognition as sr
# import pyttsx3


#========================================
# DISPLAY CONFIGURATIONS
#========================================

BODY = (  # <-- Used in rendering of graphic
  [r'     ',r'     ',r'     ',r'     ',r'     '],
  [r'  O  ',r'     ',r'     ',r'     ',r'     '],
  [r'  O  ',r'  |  ',r'  |  ',r'     ',r'     '],
  [r'\ O  ',r' \|  ',r'  |  ',r'     ',r'     '],
  [r'\ O /',r' \|/ ',r'  |  ',r'     ',r'     '],
  [r'\ O /',r' \|/ ',r'  |  ',r' /   ',r'/    '],
  [r'\ O /',r' \|/ ',r'  |  ',r' / \ ','/   \\'])

# Section title
def show_title(text):
  length = len(text) + 2
  title = [f"/*{'='*length}",f"| {text.upper()} |",f"{'='*length}*/"]
  for i in title:
    print(i)

# Title screen to be display when app initializes
def title_screen(BODY):
  screen = [
    f"/*{'='*22}*\\",
    f"|  {'hangman'.upper().ljust(15)}{BODY[6][0]}  |",
    f"|  {'for the CLI'.ljust(15)}{BODY[6][1]}  |",
    f"|  {' '.ljust(15)}{BODY[6][2]}  |",
    f"|  {'Made by:'.ljust(15)}{BODY[6][3]}  |",
    f"|  {'J.D.'.ljust(15)}{BODY[6][4]}  |",
    f"\\*{'='*22}*/",
  ]
  for i in screen:
    print(i)
  print()

def get_menu_options(menu):
  show_options(menu)
  selection = get_selection(menu)
  print()
  print(f"You have chosen to `{selection.label}`")
  return selection


#========================================
# MENU CONFIGURATION
#========================================

class MenuOption:
  def __init__(self, name:str, label:str, action):
    self.name = name
    self.label = label
    self.action = action

  def __str__(self):
    return f"<MenuOption `{self.name.upper()}` (Callback: {self.action})>"

  def __repr__(self):
    return f"MenuOption(name='{self.name}', label='{self.label}', action='{self.action}')"

# Callback Func: `START` (Menu Option = 1)
def start_game():
  """
  Creates a new instance of a `Game` 
  object for a user-specified game mode
  """
  mode = get_mode(modes)
  print()
  new = Game(mode)
  new.make_word()
  new.play()
  time.sleep(10)

# Callback Func: `RULES` (Menu Option = 2)
def show_rules():
  mode = get_mode(modes)
  print()
  show_title("rules")
  print()
  width = 80
  rules = {
    'game mode':f"{mode.name.upper()} -- {mode.label.title()}",
    'objective':fill(mode.objective, width=width),
    'gameplay':fill("The mystery word is depicted by a row of dashes, representing each letter of the word. Guess a letter that occurs in the mystery word. If it is correct, all occurences will be displayed. If it is incorrect, a body part will appear in the diagram. The game is won by guessing all correct letters in the mystery word before the diagram is complete.", width=width),
    'parameters':f"Word Source: {mode.source} | Timed?: {mode.hasTimer} | Max Errors: {mode.max_errors}"
  }
  for k,v in rules.items():
    print(f"{k.title()}:")
    print(v)
    print()
  time.sleep(20)

# Callback Func: `END` (Menu Option = 3)
def end_app():
  print("I hope you enjoyed this game. Have a great day!")
  sys.exit(0)

# `MenuOption` instances
start = MenuOption("start", "Start a New Game", start_game)
rules = MenuOption("rules", "Show the Rules", show_rules)
end = MenuOption("end", "End the Application", end_app)

# Menu Items
menu = [start,rules,end]


#========================================
# MODE CONFIGURATION
#========================================

class Mode:
  def __init__(self, name, label, objective=None, source=None, hasTimer:bool=False, max_errors:int=6):
    self.name = name
    self.label = label
    self.objective= objective
    self.source = source
    self.hasTimer = hasTimer
    self.max_errors = max_errors
    self._word = ""
    self._chars = ()
    self._blanks = []

  def __str__(self):
    return f"<Mode `{self.name.title()}` (Params = Source: {self.source}, Timed?: {self.hasTimer}, Max Errors: {self.max_errors})`>"

  def __repr__(self):
    return f"Mode(name='{self.name}', label='{self.label}')"

  @staticmethod
  def from_dictionary():
    pass
    # TODO: Write a function that imports a random list of words from an actual dictionary module

  @staticmethod
  def from_speech():
    pass
    # TODO: Write a function that records audio clip and transcribes words to a list

  def get_word(self):  # <-- should this be a classmethod?
    if self.source == "library":
      # words = self.from_dictionary()
      None
    elif self.source == "speech":
      # words = self.from_speech()
      None
    else:
      words = ["sandbox","resurrection","divergent","establishment","ridiculous","collection","experimentation",]
    self.word = random.choice(words).lower()
    self.chars = set(self.word)
    self.blanks = ["_" for _ in self.word]

# `Mode` instances
standard = Mode(
  "standard",
  "traditional game",
  "Determine the mystery word before reaching the maximum number of errors.",)
timed = Mode(
  "timed",
  "just in time",
  "Determine the mystery word before the time limit expires.",
  hasTimer=True,)
speech = Mode(
  "speech",
  "listen up!",
  "Determine a mystery word that is randomly chosen from an audio clip of the user's speech.",
  "speech",)

# Game Modes
modes = [standard,timed,speech]

def get_mode(modes):
  title = "game modes"
  show_title(title)
  print()
  show_options(modes)
  mode = get_selection(modes)
  print()
  print(f"You have selected the `{str(mode.name).title()}` game mode.")
  return mode


#========================================
# GAMEPLAY CONFIGURATION
#========================================

class Guess():
  def __init__(self, value:str="", BODY=BODY):
    self.value = value
    self.BODY = BODY
    self.hits = []
    self.misses = []

  def __str__(self):
    return self.value
  
  def __repr__(self):
    return f"Guess(value='{self.value}')"

  def is_valid(self, target):
    return str(self.value).isalpha() and (len(self.value) == 1 or len(self.value) == len(target))

  @property
  def is_unique(self):
    if self.value in self.misses or self.value in self.hits:
      print("You already used this guess.")
    return not(self.value in self.misses or self.value in self.hits)

  def get_guess(self, target):
    valid = False
    while not valid:
      self.value = input("Enter a single letter that is in the target word, or the entire word itself: ").lower()
      valid = self.is_valid(target) and self.is_unique
    return self.value.lower()

  def is_in_word(self, word):
    return word.find(self.value) != -1

  def is_word(self, word):
    return self.value == word

  def hit_string(self, target, arr):
    for idx in range(len(target)):
      if len(self.value) == 1 and self.value == target[idx]:
        arr[idx] = self.value.upper()
      if self.value == target:
        arr = [char.upper() for char in self.value]
    return " ".join(arr)

  def miss_string(self):
    return ", ".join(self.misses).upper()

  def show_board(self, h_string, m_string):
    err = len(self.misses)
    placeholder = [
      f"{'_'*5}[]".rjust(11),
      f"{'I'.center(9)}{'||'.ljust(6)}Word:   {h_string}",
      f"{'I'.center(9)}{'||'.ljust(6)}",
      f"{self.BODY[err][0].center(9)}{'||'.ljust(6)}",
      f"{self.BODY[err][1].center(9)}{'||'.ljust(6)}Guess:  {self.value.upper()}",
      f"{self.BODY[err][2].center(9)}{'||'.ljust(6)}",
      f"{self.BODY[err][3].center(9)}{'||'.ljust(6)}",
      f"{self.BODY[err][4].center(9)}{'||'.ljust(6)}Misses: {m_string}",
      f"{' '*9}{'||'.ljust(6)}",
      f"{' '*9}{'||'.ljust(6)}",
      f"[{'='*8}[]",
    ]
    for i in placeholder:
      print(i)

class Game:
  def __init__(self, m_obj=standard, *args):  # <-- `m_obj` is the user-selected game mode 
    self.m_obj = m_obj
    self._source = m_obj.source
    self._hasTimer = m_obj.hasTimer
    self._max_errors = m_obj.max_errors
    self._mystery = ""
    self._mystery_chars = {}
    self._blanks = []

  def make_word(self):
    mode = copy.copy(self.m_obj)
    mode.get_word()
    self._mystery = mode.word
    self._mystery_chars = mode.chars
    self._blanks = mode.blanks
    print(f"The mystery word contains {len(self._mystery)} letters.")
    print()

  @staticmethod
  def praise():
    praise = ["Success","Fantastic","Awesome","Phenomenal"]
    return random.choice(praise).title() + "!"

  @staticmethod
  def taunt():
    taunt = ["Tough luck.","You can do better.","You're joking, right?!","Aww... so close."]
    return random.choice(taunt)

  def play(self):
    g = Guess()
    while len(g.misses) < self._max_errors and len(g.hits) < len(self._mystery_chars):
      isRepeated = True
      while isRepeated:
        g.get_guess(self._mystery)
        isRepeated = not g.is_unique
      if len(g.value) == 1 and g.is_in_word(self._mystery):
        g.hits.append(g.value)
        print(self.praise())
      elif len(g.value) == len(self._mystery) and g.is_word(self._mystery):
        g.hits.clear()
        g.hits.extend([char for char in g.value])
        print(self.praise())
      else:
        g.misses.append(g.value)
        print(self.taunt())
      print()
      h_string = g.hit_string(self._mystery, self._blanks)
      m_string = g.miss_string()
      g.show_board(h_string,m_string)
      print()
      print()
    print(f"The correct word was `{self._mystery.upper()}`.")
    if len(g.hits) == len(self._mystery):
      print("Congratulations. You won the game!")
    if len(g.misses) == self._max_errors:
      print("Whomp whomp. You lose! Better luck next time.")


#========================================
# HELPER FUNCTIONS
#========================================

def is_obj_valid(selection, obj_array):
  if selection.isdigit() and int(selection)-1 in range(len(obj_array)):
    idx = int(selection)-1
    return True, obj_array[idx]
  elif selection in [str(obj.name).lower() for obj in obj_array]:
    for obj in obj_array:
      if selection == str(obj.name).lower():
        return True, obj
  else:
    print(f"The selected option ({selection}) is invalid. Try again.")
    return False, None

def show_options(obj_array):
  for obj in obj_array:
    print(f"{obj_array.index(obj)+1} -- {str(obj.name).upper()} ({str(obj.label).title()})")

def get_selection(obj_array):
  is_valid = False
  while not is_valid:
    selection = input("Select one of the options above: ").lower()
    is_valid, obj = is_obj_valid(selection, obj_array)
  return obj


#========================================
# MAIN APPLICATION
#========================================

def run_app():
  title_screen(BODY)
  obj = get_menu_options(menu)
  print()
  obj.action()
  print()
  print(f"<*x{'='*80}x*>")  # <-- border
  return obj

def hangman():
  action = None
  while action != end:
    action = run_app()
    print()
  print("Thanks for using the app!")



if __name__ == '__main__':
  hangman()



# Display Corpse
def display_corpse():
  print(rf"""
      _____[]
      I    ||
      I    ||
    \ O /  ||
     \|/   ||
      |    ||
     / \   ||
    /   \  ||
           ||
           ||
  [========[]
  """)