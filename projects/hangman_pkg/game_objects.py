import random
import asyncio
import pyttsx3
import speech_recognition as sr


#========================================
# MENU CONFIGURATION
#========================================

class Option:
  """
  A class for a menu option of Hangman

  Attribute(s)
  ------------
  name : str
      The internal name assigned to a game mode
  label : str
      The colloquial name of the game
      mode displayed to a user
  action : func
      A callback function to execute
      the selected menu option

  Class Variable(s)
  -----------------
  menu = list
      A list of all instantiated 'Option' objects

  """
  menu = []

  def __init__(self, name:str, label:str, action):
    self.name = name
    self.label = label
    self.action = action
    Option.menu.append(self)

  def __str__(self):
    return f"{self.name.upper()}"

  def __repr__(self):
    param_str = ", ".join(f"{k}='{v}'" for k,v in vars(self).items())
    return f"{self.__class__.__name__}({param_str})"


#========================================
# GAMEPLAY CONFIGURATION
#========================================

class Game:
    """
    A superclass for a game instance of Hangman


    Attribute(s)
    ------------
    is_victorious : bool
        Indicates whether or not a player
        won an instance of a game

    Class Variable(s)
    -----------------
    victories = dict
        A dictionary that maintains a tally
        for the number of wins per game mode
        played during an app session
    
    Method(s)
    ---------
    * speak(text)
    * communicate(bool, func1, func2, text)
    * praise()
    * taunt()

    """
    victories = {}

    def __init__(self, is_victorious=False):
        self.is_victorious = is_victorious

    @staticmethod
    def speak(text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    @staticmethod
    def communicate(bool, func1, func2, text):
        func1(text) if bool else  func2(text)

    @staticmethod
    def praise():
        praise = ["Success","Fantastic","Awesome","Phenomenal"]
        return random.choice(praise) + "!"

    @staticmethod
    def taunt():
        taunt = ["Tough luck.","Bollocks, you can do better.","Are you serious?!","Aww... so close."]
        return random.choice(taunt)

    @classmethod
    def summary(cls):
      print("Gameplay Summary".center(27))
      print(f"/{'-'*25}\\")
      for k, v in Game.victories.items():
        print(f"| {k.title().rjust(8)} Mode: {str(sum(v)).zfill(2)} of {str(len(v)).zfill(2)} |")
      print(f"\{'_'*25}/")
      print("\n\n")


class Mode(Game):
    """
    A subclass of `Game`. Represents a 
    specific game mode in Hangman with
    custom gameplay parameters

    Attribute(s)
    ------------
    is_victorious : bool
        Indicates whether or not a player
        won an instance of a game mode
    name : str
        The internal name assigned to a game mode
    label : str
        The colloquial name of the game
        mode displayed to a user
    objective : str
        A brief description of the objective for the selected game mode
    source : str
        The word source for a selected game mode
    word_length : int
        The minimum length for a mystery word
    has_timer : bool
        Indicates whether or not an instance
        of the game mode is timed
    max_errors : int
        The maximum number of errors a
        user is allowed to make before
        losing the game
    word : str
        An unknown mystery word determined 
        by the selected game mode
    chars : set
        A set of all unique letters contained
        in the mystery word
    blanks : list
        A list of placeholders (underscores)
        equal to the length of the mystery word

    Class Variable(s)
    -----------------
    all_modes = list
        A list of all instantiated 'Mode' objects

    Method(s)
    ---------
    * contact_local_dicitionary
    * get_from_dictionary
    * eavesdrop
    * get_from_speech
    * get_word

    """
    all_modes = []

    def __init__(
        self, is_victorious, 
        name, label, 
        objective=None, source=None, word_length=8,has_timer:bool=False, max_errors:int=6):
        super().__init__(is_victorious)
        self.is_victorious =is_victorious
        self.name = name
        self.label = label
        self.objective = objective
        self.source = source
        self.word_length = word_length
        self.has_timer = has_timer
        self.max_errors = max_errors
        self._word = ""
        self._chars = set(self._word)
        self._blanks = ["_" for _ in self._word]
        Mode.all_modes.append(self)

    def __str__(self):
        return f"{self.name.upper()}"

    def __repr__(self):
        param_str = ", ".join(f"{k}='{v}'" for k,v in vars(self).items())
        return f"{self.__class__.__name__}({param_str})"

    def contact_local_dicitionary(self):
        outcome = {  # <-- response object
            'words': None,
            'successful': True,
            'error': None,
        }
        try:
            with open("/usr/share/dict/words", "r") as f:
                raw_list = f.read().split("\n")
                filtered_list = [word for word in raw_list if (len(word) >= self.word_length 
                and word[0].islower())]
        except:
            outcome["successful"] = False
            outcome["error"] = "I cannot reach the local system dictionary!"
        else:
            outcome["words"] = filtered_list
        finally:
            return outcome

    def get_from_dictionary(self):
        outcome = self.contact_local_dicitionary()
        return outcome['words']

    def eavesdrop(self):
        """
        This function will transcribe speech recorded from the
        user's voice and return a dictionary with data from
        this operation: word array and errors (if applicable)

        () -> dict
        """
        r = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:  # <-- record audio from microphone
            r.adjust_for_ambient_noise(source, 2)
            audio = r.listen(source)

        outcome = {  # <-- response object
            'words': None,
            'successful': True,
            'error': None,
        }
        try:  # <-- recognize speech w/ Google Speech Recognition
            raw_word_list = r.recognize_google(audio).lower().split(" ")
            outcome['words'] = list(filter(lambda word: len(word) >= self.word_length, raw_word_list))
        except sr.UnknownValueError:
            outcome['successful'] = False
            outcome['error'] = "I cannot recognize your speech"
        except sr.RequestError as e:
            outcome['successful'] = False
            outcome['error'] = "I cannot contact the API"
        # try:  # <-- recognize speech w/ Sphinx
        #   raw_word_list = r.recognize_sphinx(audio).lower().split(" ")
        # except sr.UnknownValueError:
        #   print("Sphinx could not understand audio")
        # except sr.RequestError as e:
        #   print(f"Could not request results from Sphinx; {e}")
        return outcome

    def get_from_speech(self):
        while True:
            self.speak("Speak naturally and clearly for up to 30 seconds.")
            outcome = self.eavesdrop()
            words = outcome['words']
            if words:
                self.speak("Alright, you've said enough. Let the game begin.")
                return words
            elif "speech" in outcome['error']:
                self.speak(f"{outcome['error']}. Don't be shy. Please speak up and try again.")
                continue
            else:
                self.speak(f"{outcome['error']}. Please return to the main menu and select a different game mode.")
                return None

    def get_word(self):
        DEFAULT_WORDS = [
            "sandbox","resurrection","divergent","establishment","ridiculous","collection","experimentation",]
        if self.source == "dictionary":
            words = self.get_from_dictionary()
        elif self.source == "speech":
            words = self.get_from_speech()
        if not self.source or (not words and self.source):
            words = DEFAULT_WORDS
        self._word = random.choice(words).lower()
        for char in self._word:
            self._chars.add(char)
        self._blanks = ["_" for _ in self._word]
        self.communicate(self.source == "speech", self.speak, print, f"The mystery word contains {len(self._word)} letters.")

    def play(self):
      if not self.name in Game.victories.keys():
        Game.victories[self.name] = []
      does_game_speak = self.source == "speech"
      g = Guess()
      while len(g.misses) < self.max_errors and len(g.hits) < len(self._word):
        is_repeated = True
        while is_repeated:
          g.get_guess(self._word, does_game_speak)
          is_repeated = not g.is_unique
        if len(g.value) == 1 and g.is_in_word(self._word):
          g.hits.append(g.value)
          self.communicate(does_game_speak, self.speak, print, self.praise())
        elif len(g.value) == len(self._word) and g.is_word(self._word):
          g.hits.clear()
          g.hits.extend([char for char in g.value])
          self.communicate(does_game_speak, self.speak, print, self.praise())
        else:
          g.misses.append(g.value)
          self.communicate(does_game_speak, self.speak, print, self.taunt())
        print()
        h_string = g.hit_string(self._word, self._blanks)
        m_string = g.miss_string()
        g.show_board(h_string, m_string)
        print()
        print()
        if len(set(g.hits)) == len(set([char for char in self._word])) or len(g.misses) == self.max_errors:
          break
      self.communicate(does_game_speak, self.speak, print, f"The correct word was `{self._word.upper()}`.")
      if len(set(g.hits)) == len(set([char for char in self._word])):
        self.communicate(does_game_speak, self.speak, print, "Congratulations. You won the game!")
        self.is_victorious = True
      if len(g.misses) == self.max_errors:
        self.communicate(does_game_speak, self.speak, print, "Whomp whomp. You lose! Better luck next time.")
      Game.victories[self.name].append(self.is_victorious)

# `Mode` instances
standard = Mode(
  False,
  "standard",
  "traditional game",
  "Determine the mystery word before reaching the maximum number of errors.",
  "dictionary")
timed = Mode(
  False,
  "timed",
  "just in time",
  "Determine the mystery word before the time limit expires.",
  has_timer=True,)
speech = Mode(
  False,
  "speech",
  "listen up!",
  "Determine a mystery word that is randomly chosen from an audio clip of the user's speech.",
  "speech",)


class Guess():
  """
  A class that represents a user's guesses
  of the mystery word generated by an
  instance of the 'Mode' class
  
  Attribute(s)
  ------------
  value : str
      The value of a user's current guess. It
      may be either a single character or a 
      word whose length is exactly equal to that
      of the mystery word
  hits : list
      A list of all distinct letters contained
      within the mystery word that are guessed
      correctly by the user. The list may also include the actual mystery word.
  misses : list
      A list of all distinct letters that are
      not contained within the mystery word that are guessed by the user. The list may also include 
      whole words that are equal in length to
      the mystery word.
  
  Class Variable(s)
  -----------------
  BODY = tuple
      A container for the components of the 
      'hangman' graphic that is displayed to
      a user in the command line
  
  Property
  ---------
  * is_unique

  Method(s)
  ---------
  * get_guess
  * is_in_word
  * is_word
  * hit_string
  * miss_string
  * show_board

  """
  BODY = (
  [r'     ',r'     ',r'     ',r'     ',r'     '],
  [r'  O  ',r'     ',r'     ',r'     ',r'     '],
  [r'  O  ',r'  |  ',r'  |  ',r'     ',r'     '],
  [r'\ O  ',r' \|  ',r'  |  ',r'     ',r'     '],
  [r'\ O /',r' \|/ ',r'  |  ',r'     ',r'     '],
  [r'\ O /',r' \|/ ',r'  |  ',r' /   ',r'/    '],
  [r'\ O /',r' \|/ ',r'  |  ',r' / \ ','/   \\'])

  def __init__(self, value:str=""):
    self.value = value
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

  @staticmethod
  def speak(text):
      engine = pyttsx3.init()
      engine.say(text)
      engine.runAndWait()

  def listen(self, *args):
    target = args[0] if args else None
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:  # <-- record audio from microphone
        r.adjust_for_ambient_noise(source, 0.5)
        audio = r.listen(source)
    outcome = None
    try:  # <-- recognize speech w/ Google Speech Recognition
        outcome = r.recognize_google(audio).lower().split(" ")[0]
    except sr.UnknownValueError:
        self.speak("I cannot recognize your speech.")
        return outcome
    except sr.RequestError as e:
        self.speak("I cannot contact the API.")
        return outcome
    else:
        if outcome == target:
          self.speak(f"Did you say {outcome}? Say 'yes' or 'no' to confirm.")
          confirmation = self.listen("yes")
        return outcome if (outcome == target and confirmation == "yes") else outcome[0]

  def get_guess(self, target, *args):
    is_speaking = args[0] if args else None
    base_prompt = f"{'Say' if is_speaking else 'Enter'} a single letter in the target word, or {'say' if is_speaking else 'enter'} the entire word itself: "
    alt_prompt = "It would seem that I may have difficulty understanding you clearly. As an alternative, please state a word from the phonetic alphabet and I will extract the first letter of the word I hear as your guess."
    valid = False
    err_count = 0
    while not valid:
      if is_speaking:
        self.speak(base_prompt if err_count == 0 else alt_prompt)
        # if err_count == 0:
        #   self.speak(base_prompt)
        # else:
        #   self.speak(alt_prompt)
        self.value = self.listen(target)
        print(str(self.value)) # debugging
        if self.value == None:
          err_count += 1
          continue
      else:
        self.value = input(base_prompt).lower()
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

