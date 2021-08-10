import random
# import os, platform
# import speech_recognition as sr
# import pyttsx3




#----------------------------------------
# GAMEPLAY CONFIGURATION
#----------------------------------------

def dictionaryWord():
  pass
  # TODO: Write a function that imports a random list of words from an actual dictionary


def speechToText():
  pass
  # TODO: Write a function that records audio clip and transcribes words to a list 


# Select a random guess word from mode-specific source
def chooseWordFrom(source):
  """
  Selects a random word from a
  pre-defined list of words

  () -> str, set
  """
  if source == "library":
    # words = dictionaryWord()  <-- Needs to be implemented in production
    words = [
      "sandbox",
      "resurrection",
      "divergent",
      "establishment",
      "ridiculous",
      "collection",
      "experimentation",
    ]
  # elif source == "speech":
    # words = speechToText()  <-- Needs to be implemented in production
  else:
    words = [
      "sandbox",
      "resurrection",
      "divergent",
      "establishment",
      "ridiculous",
      "collection",
      "experimentation",
    ]
  word = random.choice(words).lower()
  wordChars = set(word)
  print(f"The guess word contains {len(word)} letters.\n")
  return word, wordChars


# Check if guess is a single letter or length of `guessWord`
def isGuessValid(guess,guessWord):
  if not(guess.isalpha() and (len(guess) == 1 or len(guess) == len(guessWord))):
    print(f"The selected guess ({guess}) is invalid. Try again.")
    return False
  return True


# Get guess from user
def getUserGuess(guessWord):
  valid_guess = False
  while(not valid_guess):
    guess = input("Enter a single letter that is in the guess word, or the entire word itself: ")
    valid_guess = isGuessValid(guess,guessWord)
  return guess.lower()


# Check if user repeated guess
def isGuessUnique(guess,misses,hits):
  isUnique = not(guess in misses or guess in hits)
  if not isUnique:
    print(f"You already selected `{guess}` as a previous guess. Try again.")
  return isUnique


# Check if `guess` is in `guessWord`
def isGuessInWord(guess,guessWord):
  if guessWord.find(guess) != -1:
    return True
  return False


# Check if `guess` is equal to `guessWord`
def isGuessWord(guess,guessWord):
  if guess == guessWord:
    return True
  return False


# Traditional gameplay
def standardGame(wordSource):
  guessWord, guessWordChars = chooseWordFrom(wordSource)
  placeholder = ["_" for _ in guessWord]
  maxAttempts = len(bodyParts) - 1
  attempts = 0
  misses = []
  hits = []
  while len(misses) < maxAttempts and len(hits) < len(guessWordChars):
    isRepeatedGuess = True
    while isRepeatedGuess:
      guess = getUserGuess(guessWord)
      isRepeatedGuess = not isGuessUnique(guess,misses,hits)
    if len(guess) == 1 and isGuessInWord(guess,guessWord):  # <- Action if user guesses correct letter
      hits.append(guess)
      print(displayPraise())
    elif len(guess) == len(guessWord) and isGuessWord(guess,guessWord):  # <- Action is user guesses correct word
      hits.clear()
      hits.extend(set([char for char in guess]))
      print(displayPraise())
    else:
      misses.append(guess)
      attempts = len(misses)
      print(displayTaunt())
    showBoard(bodyParts,attempts,guessWord,guess,misses,placeholder)
    print()
  print(f"The correct word was `{guessWord.upper()}`.")
  if len(hits) == len(guessWordChars):
    print("Congratulations. You won the game!")
  if len(misses) == maxAttempts:
    print("Whomp whomp. You lose! Better luck next time.")


# Timed gameplay
def timedGame():
  pass


# Speech-dependent gameplay
def speechGame():
  pass



#----------------------------------------
# DISPLAY CONFIGURATION
#----------------------------------------

bodyParts = {
  0: [r'     ',r'     ',r'     ',r'     ',r'     '],
  1: [r'  O  ',r'     ',r'     ',r'     ',r'     '],
  2: [r'  O  ',r'  |  ',r'  |  ',r'     ',r'     '],
  3: [r'\ O  ',r' \|  ',r'  |  ',r'     ',r'     '],
  4: [r'\ O /',r' \|/ ',r'  |  ',r'     ',r'     '],
  5: [r'\ O /',r' \|/ ',r'  |  ',r' /   ',r'/    '],
  6: [r'\ O /',r' \|/ ',r'  |  ',r' / \ ','/   \\']
}


def displayPraise():
  praise = ["Success","Fantastic","Awesome","Phenomenal"]
  return random.choice(praise).title() + "!"


def displayTaunt():
  taunt = ["Tough luck.","You can do better.","You're joking, right?!","Aww... so close."]
  return random.choice(taunt)


def displayPlaceholder(guessWord,guess,arr):
  """
  Replaces underscores in `guessWord` placeholder
  with a correct `guess` in all occurences

  (str,char,list) -> list
  """
  for idx in range(len(guessWord)):
    if len(guess) == 1 and guess == guessWord[idx]:
      arr[idx] = guess.upper()
    if guess == guessWord:
      arr = [char.upper() for char in guess]
  return arr


def displayMisses(misses):
  """
  Display list items in `misses` as a
  single comma-separated string

  (list) -> str
  """
  return ', '.join(misses).upper()


def showBoard(bodyParts,attempt,guessWord,guess,misses,placeholder):
  """
  Displays the game board for each
  new guess made by the user
  """
  display = displayPlaceholder(guessWord,guess,placeholder)
  print(
rf"""
    _____[]
    I    ||    Word:   {' '.join(display)}
    I    ||
  {bodyParts[attempt][0]}  ||
  {bodyParts[attempt][1]}  ||    Guess:  {guess.upper()}
  {bodyParts[attempt][2]}  ||
  {bodyParts[attempt][3]}  ||
  {bodyParts[attempt][4]}  ||    Misses: {displayMisses(misses)}
         ||
         ||
[========[]
"""
  )



#----------------------------------------
# APPLICATION CONFIGURATIONS
#----------------------------------------

# Create a new game instance (Menu Option = 1)
def newGame():
  """
  Creates a new instance of a game
  for a user-specified game mode
  """
  mode = getGameMode(gameModes)
  wordSource = gameModes[mode]['source'] 
  print()
  gameModes[mode]['action'](wordSource)


# Display rules for selected game mode (Menu Option = 2)
def displayRules():
  """
  Displays the rules for a game
  user-specified game mode
  """
  mode = getGameMode(gameModes)
  print(rf"""
/*======= 
| RULES |
=======*/

Game Mode: 
<< {gameModes[mode]['name'].title()} >>

Objective: 
{gameModes[mode]['objective']}

Gameplay:
The mystery word is depicted by a row of dashes, representing each letter of the word.
Guess a letter that occurs in the mystery word. If it is correct, all occurences will
be displayed. If it is incorrect, a body part will appear in the diagram. The game is
won by guessing all correct letters in the mystery word before the diagram is complete.

Constraints:
{gameModes[mode]['constraints']}
  """)


# Exit the application (Menu Option = 3)
def exitApp():
  print("We hope you enjoyed this app. Have a great day!")


# Title screen to be dsiplay when app initializes
def displayTitleScreen(bodyParts):
  print(rf"""
/*=======================*\
|  HANGMAN         {bodyParts[6][0]}  |
|  for the CLI     {bodyParts[6][1]}  |
|                  {bodyParts[6][2]}  |
|  Made by:        {bodyParts[6][3]}  |
|  J.D.            {bodyParts[6][4]}  |
\*=======================*/
  """)


menuOptions = {
  '1': {
    'name':"Start a New Game",
    'action': newGame,
    },
  '2': {
    'name':"Display the Rules",
    'action': displayRules,
    },
  '3': {
    'name':"Exit the Application",
    'action': exitApp
    },
}
def getMenuSelection(menuOptions):
  displayOptions(menuOptions)
  selection = getUserSelection(menuOptions)
  print()
  print(f"You have chosen to `{menuOptions[selection]['name']}`")
  return selection


# TODO: Refactor `gameModes` dictionary into objects of a 'Mode' class
gameModes = {
  '1': {
    'name':"standard",
    'action':standardGame,
    'objective':"Determine the mystery word before the maximum number of guesses are exhausted.",
    'source': "library",
    'hasTimer': False,
    'constraints': None,
  },
  '2': {
    'name':"just in time",
    'action': timedGame,
    'objective':"Determine the mystery word before the time limit expires.",
    'source':"library",
    'hasTimer': True,
    'constraints': None,
  },
  '3': {
    'name':"listen up!",
    'action':speechGame,
    'objective':"Determine a mystery word that is randomly recorded from a clip of the user's speech.",
    'source':"speech",
    'hasTimer': False,
    'constraints': None,
  },
}
def getGameMode(gameModes):
  print(r"""
/*====================
| HANGMAN GAME MODES |
====================*/
  """)
  displayOptions(gameModes)
  mode = getUserSelection(gameModes)
  print()
  print(f"You have selected the `{gameModes[mode]['name'].title()}` game mode.")
  return mode



#----------------------------------------
# HELPER FUNCTIONS
#----------------------------------------

def isOptionValid(choice, options):
  """
  Checks if `user_choice` is a key
  in the `options` dictionary

  (str,dict) -> bool
  """
  if choice not in options.keys():
    print(f"The selected option ({choice}) is invalid. Try again.")
    return False
  else:
    return True


def displayOptions(options):
  """
  Displays game options to the user at
  the beginning of the application

  (dict) -> None
  """
  for option, value in options.items():
    print(f"{option} -- {value['name'].upper()}")


def getUserSelection(options):
  """
  Obtains and validates a 
  user's selected option

  (dict) -> str
  """
  valid_choice = False
  while(not valid_choice):
    selection = input("Select one of the options above: ")
    valid_choice = isOptionValid(selection, options)
  return selection


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


#----------------------------------------
# MAIN APPLICATION
#----------------------------------------

def hangman():
  displayTitleScreen(bodyParts)
  menuSelection = getMenuSelection(menuOptions)
  print()
  menuOptions[menuSelection]['action']()

hangman()