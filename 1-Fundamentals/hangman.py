import random
# import os, platform
# import speech_recognition as sr
# import pyttsx3




#----------------------------------------
# GAMEPLAY CONFIGURATION
#----------------------------------------


# Select a random guess word from a list
def chooseRandomWord():
  """
  Selects a random word from a
  pre-defined list of words

  () -> str, set
  """
  words = [
    "sandbox",
    "resurrection",
    "divergent",
    "establishment",
  ]
  word = random.choice(words).lower()
  wordChars = set(word)
  print(f"The guess word contains {len(word)} letters.\n")
  return word, wordChars


# Get guess from user
def getUserGuess():
  valid_guess = False
  while(not valid_guess):
    guess = input("Enter a single letter that is in the guess word: ")
    valid_guess = isGuessValid(guess)
  return guess.lower()


# Check if `guess` is in `guessWord`
def isGuessInWord(guess,guessWord):
  if guessWord.find(guess) != -1:
    return True
  return False


# Check if user repeated guess
def isGuessUnique(guess,misses,hits):
  isUnique = not(guess in misses or guess in hits)
  if not isUnique:
    print(f"You already selected `{guess}` as a previous guess. Try again.")
  return isUnique


# Check if guess is a single letter
def isGuessValid(guess):
  if not(guess.isalpha() and len(guess) == 1):
    print(f"The selected guess ({guess}) is invalid. Try again.")
    return False
  return True


def playGame():
  maxAttempts = len(bodyParts) - 1
  attempts = 0
  misses = []
  hits = []
  guessWord, guessWordChars = chooseRandomWord()
  placeholder = ["_" for _ in guessWord]
  while len(misses) < maxAttempts and len(hits) < len(guessWordChars):
    isRepeatedGuess = True
    while isRepeatedGuess:
      guess = getUserGuess()
      isRepeatedGuess = not isGuessUnique(guess,misses,hits)
    if isGuessInWord(guess,guessWord):
      hits.append(guess)
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
  taunt = ["Tough luck.","You can do better.","You're joking, right?!"]
  return random.choice(taunt)


def displayPlaceholder(guessWord,guess,arr):
  for idx in range(len(guessWord)):
    if guess == guessWord[idx]:
      arr[idx] = guess.upper()
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
# APPLICATION FUNCTIONS
#----------------------------------------
def newGame():
  print("This will begin a new game")
  # TODO: Write function for a new game instance

def displayRules():
  print("This will display the rules")
  # TODO: Write function to display game rules

def exitApp():
  print("We hope you enjoyed this app. Have a great day!")

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
    selection = input("Select one of the menu options above: ")
    valid_choice = isOptionValid(selection, options)
  return selection


def hangman():
  menuOptions = {
  '1': {
    'name':"Start a New Game",
    'action': playGame,
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
  displayOptions(menuOptions)
  user_choice = getUserSelection(menuOptions)
  print()
  print(f"You have chosen to `{menuOptions[user_choice]['name']}`")
  menuOptions[user_choice]['action']()

hangman()


# CORPSE
rf"""
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
"""