from hangman_pkg.config import *
from hangman_pkg.game_objects import *

import sys
from textwrap import fill, wrap
import time
import copy


#========================================
# MENU CONFIGURATION
#========================================

# Callback Func: `START` (Menu Option = 1)
def start_game():
  """
  Creates a new instance of a game 'Mode'
  and initiates gameplay
  """
  mode = get_mode()
  print()
  mode.get_word()
  mode.play()
  print()
  Game.summary()
  time.sleep(10)

# Callback Func: `RULES` (Menu Option = 2)
def show_rules():
  mode = get_mode()
  print()
  show_title("rules")
  print()
  width = 80
  rules = {
    'game mode':f"{mode.name.upper()} -- {mode.label.title()}",
    'objective':fill(mode.objective, width=width),
    'gameplay':fill("The mystery word is depicted by a row of dashes, representing each letter of the word. Guess a letter that occurs in the mystery word. If it is correct, all occurences will be displayed. If it is incorrect, a body part will appear in the diagram. The game is won by guessing all correct letters in the mystery word before the diagram is complete.", width=width),
    'parameters':f"Word Source: {mode.source} | Timed?: {mode.has_timer} | Max Errors: {mode.max_errors}"
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

# `Option` instances
start = Option("start", "Start a New Game", start_game)
rules = Option("rules", "Show the Rules", show_rules)
end = Option("end", "End the Application", end_app)

def get_mode():
  title = "game modes"
  show_title(title)
  print()
  show_options(Mode.all_modes)
  mode = get_selection(Mode.all_modes)
  new_mode = copy.copy(mode)
  print()
  print(f"You have selected the `{str(new_mode.name).title()}` game mode.")
  return new_mode


#========================================
# MAIN APPLICATION
#========================================

def run_app():
  title_screen()
  obj = get_menu_options(Option.menu)
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
