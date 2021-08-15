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
def showTitle(text):
  length = len(text) + 2
  title = [f"/*{'='*length}",f"| {text.upper()} |",f"{'='*length}*/"]
  for i in title:
    print(i)

# Title screen to be dsiplay when app initializes
def displayTitleScreen(BODY):
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

def getMenuOptions(menu):
  showOptions(menu)
  selection = getSelection(menu)
  print()
  print(f"You have chosen to `{selection.label}`")
  return selection


#========================================
# MENU CONFIGURATION
#========================================

class MenuOption:
  def __init__(self,name:str,label:str,action):
    self.name = name
    self.label = label
    self.action = action

  def __str__(self):
    return self.name

  def __repr__(self):
    return f"<MenuOption `{self.name.upper()}` (Callback: {self.action})>"

# Callback Func: `START` (Menu Option = 1)
def startGame():
  """
  Creates a new instance of a `Game` 
  object for a user-specified game mode
  """
  mode = getMode(modes)
  print()
  new = Game(mode)
  new.makeWord()
  new.play()
  time.sleep(10)

# Callback Func: `RULES` (Menu Option = 2)
def showRules():
  mode = getMode(modes)
  print()
  showTitle("rules")
  print()
  width = 80
  rules = {
    'game mode':f"{mode.name.upper()} -- {mode.label.title()}",
    'objective':fill(mode.objective,width=width),
    'gameplay':fill("The mystery word is depicted by a row of dashes, representing each letter of the word. Guess a letter that occurs in the mystery word. If it is correct, all occurences will be displayed. If it is incorrect, a body part will appear in the diagram. The game is won by guessing all correct letters in the mystery word before the diagram is complete.",width=width),
    'parameters':f"Word Source: {mode.source} | Timed?: {mode.hasTimer} | Max Errors: {mode.maxErrors}"
  }
  for k,v in rules.items():
    print(f"{k.title()}:")
    print(v)
    print()
  time.sleep(20)

# Callback Func: `END` (Menu Option = 3)
def endApp():
  print("I hope you enjoyed this game. Have a great day!")
  sys.exit(0)

# `MenuOption` instances
start = MenuOption("start","Start a New Game",startGame)
rules = MenuOption("rules","Show the Rules",showRules)
end = MenuOption("end","End the Application",endApp)

# Menu Items
menu = [start,rules,end]


#========================================
# MODE CONFIGURATION
#========================================

class GameMode:
  def __init__(self,name,label,objective=None,source=None,hasTimer:bool=False,maxErrors:int=6):
    self.name = name
    self.label = label
    self.objective= objective
    self.source = source
    self.hasTimer = hasTimer
    self.maxErrors = maxErrors
    self._word = ""
    self._chars = ()
    self._blanks = []

  def __str__(self):
    return self.label.title()

  def __repr__(self):
    return f"<GameMode `{self.name.title()}` (Params = Source: {self.source}, Timed?: {self.hasTimer}, Max Errors: {self.maxErrors})`>"

  @staticmethod
  def fromDictionary():
    pass
    # TODO: Write a function that imports a random list of words from an actual dictionary module

  @staticmethod
  def fromSpeech():
    pass
    # TODO: Write a function that records audio clip and transcribes words to a list

  def getWord(self):  # <-- should this be a classmethod?
    if self.source == "library":
      # words = self.fromDictionary()
      None
    elif self.source == "speech":
      # words = self.fromSpeech()
      None
    else:
      words = ["sandbox","resurrection","divergent","establishment","ridiculous","collection","experimentation",]
    self.word = random.choice(words).lower()
    self.chars = set(self.word)
    self.blanks = ["_" for _ in self.word]

# `GameMode` instances
standard = GameMode(
  "standard",
  "traditional game",
  "Determine the mystery word before reaching the maximum number of errors.",)
timed = GameMode(
  "timed",
  "just in time",
  "Determine the mystery word before the time limit expires.",
  hasTimer=True,)
speech = GameMode(
  "speech",
  "listen up!",
  "Determine a mystery word that is randomly chosen from an audio clip of the user's speech.",
  "speech",)

# Game Modes
modes = [standard,timed,speech]

def getMode(modes):
  title = "game modes"
  showTitle(title)
  print()
  showOptions(modes)
  mode = getSelection(modes)
  print()
  print(f"You have selected the `{str(mode.name).title()}` game mode.")
  return mode


#========================================
# GAMEPLAY CONFIGURATION
#========================================

class Guess():
  def __init__(self,value:str="",BODY=BODY):
    self.value = value
    self.BODY = BODY
    self.hits = []
    self.misses = []

  def __str__(self):
    return self.value
  
  def __repr__(self):
    return self.value

  def isValid(self,target):
    return str(self.value).isalpha() and (len(self.value) == 1 or len(self.value) == len(target))

  def getGuess(self,target):
    valid = False
    while not valid:
      self.value = input("Enter a single letter that is in the target word, or the entire word itself: ")
      valid = self.isValid(target)
    return self.value.lower()

  def isUnique(self):
    return not(self.value in self.misses or self.value in self.hits)

  def inWord(self,word):
    return word.find(self.value) != -1

  def isWord(self,word):
    return self.value == word

  def hitString(self,target,arr):
    for idx in range(len(target)):
      if len(self.value) == 1 and self.value == target[idx]:
        arr[idx] = self.value.upper()
      if self.value == target:
        arr = [char.upper() for char in self.value]
    return " ".join(arr)

  def missString(self):
    return ", ".join(self.misses).upper()

  def showBoard(self,hString,mString):
    err = len(self.misses)
    placeholder = [
      f"{'_'*5}[]".rjust(11),
      f"{'I'.center(9)}{'||'.ljust(6)}Word:   {hString}",
      f"{'I'.center(9)}{'||'.ljust(6)}",
      f"{self.BODY[err][0].center(9)}{'||'.ljust(6)}",
      f"{self.BODY[err][1].center(9)}{'||'.ljust(6)}Guess:  {self.value.upper()}",
      f"{self.BODY[err][2].center(9)}{'||'.ljust(6)}",
      f"{self.BODY[err][3].center(9)}{'||'.ljust(6)}",
      f"{self.BODY[err][4].center(9)}{'||'.ljust(6)}Misses: {mString}",
      f"{' '*9}{'||'.ljust(6)}",
      f"{' '*9}{'||'.ljust(6)}",
      f"[{'='*8}[]",
    ]
    for i in placeholder:
      print(i)

class Game:
  def __init__(self,modeObj=standard,*args):
    self.modeObj = modeObj
    self._source = modeObj.source
    self._hasTimer = modeObj.hasTimer
    self._maxErrors = modeObj.maxErrors
    self._mystery = ""
    self._mysteryChars = {}
    self._blanks = []

  def makeWord(self):
    mode = copy.copy(self.modeObj)
    mode.getWord()
    self._mystery = mode.word
    self._mysteryChars = mode.chars
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
    while len(g.misses) < self._maxErrors and len(g.hits) < len(self._mysteryChars):
      isRepeated = True
      while isRepeated:
        g.getGuess(self._mystery)
        isRepeated = not g.isUnique()
      if len(g.value) == 1 and g.inWord(self._mystery):
        g.hits.append(g.value)
        print(self.praise())
      elif len(g.value) == len(self._mystery) and g.isWord(self._mystery):
        g.hits.clear()
        g.hits.extend([char for char in g.value])
        print(self.praise())
      else:
        g.misses.append(g.value)
        print(self.taunt())
      print()
      hString = g.hitString(self._mystery,self._blanks)
      mString = g.missString()
      g.showBoard(hString,mString)
      print()
      print()
    print(f"The correct word was `{self._mystery.upper()}`.")
    if len(g.hits) == len(self._mystery):
      print("Congratulations. You won the game!")
    if len(g.misses) == self._maxErrors:
      print("WHomp whomp. You lose! Better luck next time.")


#========================================
# HELPER FUNCTIONS
#========================================

def isObjValid(selection,objArray):
  if selection.isdigit() and int(selection)-1 in range(len(objArray)):
    idx = int(selection)-1
    return True, objArray[idx]
  elif selection in [str(obj.name).lower() for obj in objArray]:
    for obj in objArray:
      if selection == str(obj.name).lower():
        return True, obj
  else:
    print(f"The selected option ({selection}) is invalid. Try again.")
    return False, None

def showOptions(objArray):
  for obj in objArray:
    print(f"{objArray.index(obj)+1} -- {str(obj.name).upper()} ({str(obj.label).title()})")

def getSelection(objArray):
  isValid = False
  while not isValid:
    selection = input("Select one of the options above: ").lower()
    isValid, obj = isObjValid(selection,objArray)
  return obj


#========================================
# MAIN APPLICATION
#========================================

def runApp():
  displayTitleScreen(BODY)
  obj = getMenuOptions(menu)
  print()
  obj.action()
  print()
  print(f"<*x{'='*80}x*>")  # <-- border
  return obj

def hangman():
  action = None
  while action != end:
    action = runApp()
    print()
  print("Thanks for using the app!")

hangman()



# Display Corpse
def displayCorpse():
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