import random
import datetime

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
    history = list
        A list of all instantiated game modes
    victories = dict
        A dictionary that maintains a tally
        for the number of wins per game mode
        played during an app session
    
    Method(s)
    ---------
    * speak
    * communicate
    * praise
    * taunt
    * save_results
    * summary

    """
    history = []
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

    def save_results(self, outcome_obj):
        Game.history.append(outcome_obj)

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
    * grade_guess
    * update_user
    * results
    * play

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
        response = {  # <-- response object
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
            response["successful"] = False
            response["error"] = "I cannot reach the local system dictionary!"
        else:
            response["words"] = filtered_list
        finally:
            return response

    def get_from_dictionary(self):
        response = self.contact_local_dicitionary()
        return response['words']

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
            r.adjust_for_ambient_noise(source, 0.5)
            audio = r.listen(source)
        response = {  # <-- response object
            'words': None,
            'successful': True,
            'error': None,
        }
        try:  # <-- recognize speech w/ Google Speech Recognition
            raw_word_list = r.recognize_google(audio).lower().split(" ")
            response['words'] = list(filter(lambda word: len(word) >= self.word_length, raw_word_list))
        except sr.UnknownValueError:
            response['successful'] = False
            response['error'] = "I cannot recognize your speech"
        except sr.RequestError:
            response['successful'] = False
            response['error'] = "I cannot contact the API"
        return response

    def get_from_speech(self):
        while True:
            self.speak("Speak naturally and clearly for up to 30 seconds.")
            response = self.eavesdrop()
            words = response['words']
            if words:
                self.speak("Alright, you've said enough. Let the game begin.")
                return words
            elif "speech" in str(response['error']):
                self.speak(f"{response['error']}. Don't be shy. Please speak up and try again.")
                continue
            else:
                self.speak(f"{response['error']}. Please return to the main menu and select a different game mode.")
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

    def grade_guess(self, guess_obj):
        guess_obj.attempts.append(guess_obj.value)
        if len(guess_obj.value) == 1 and guess_obj.is_in_word(self._word):
            guess_obj.hits.append(guess_obj.value)
            return True
        elif len(guess_obj.value) == len(self._word) and guess_obj.is_word(self._word):
            guess_obj.hits.clear()
            guess_obj.hits.extend([char for char in guess_obj.value])
            return True
        else:
            guess_obj.misses.append(guess_obj.value)
            return False
        
    def update_user(self, guess_obj, correct_guess, is_speaking):
        h_string = guess_obj.hit_string(self._word, self._blanks)
        m_string = guess_obj.miss_string()
        if correct_guess:
            self.communicate(is_speaking, self.speak, print, self.praise())
        else:
            self.communicate(is_speaking, self.speak, print, self.taunt())
        guess_obj.show_board(h_string, m_string)

    def results(self, guess_obj):
        does_game_speak = self.source == "speech"
        self.communicate(does_game_speak, self.speak, print, f"The correct word was `{self._word.upper()}`.")
        if self.is_victorious:
            self.communicate(does_game_speak, self.speak, print, "Congratulations. You won the game!")
        else:
            self.communicate(does_game_speak, self.speak, print, "Whomp whomp. You lose! Better luck next time.")
        self.save_results(Outcome(self, guess_obj))

    def play(self):
        does_game_speak = self.source == "speech"
        g = Guess()
        win_clause = False
        loss_clause = False
        while not (win_clause or loss_clause):
            # Obtain and evaluate input from user
            while True:  
                if does_game_speak:
                    g.ask_guess(self._word)
                else:
                    g.get_guess(self._word)
                if g.is_unique:
                    break
            is_correct = self.grade_guess(g)
            self.update_user(g, is_correct, does_game_speak)
            print()
            print()

            # Conditions to end game
            win_clause = len(set(g.hits)) == len(set([char for char in self._word]))
            loss_clause = len(g.misses) == self.max_errors
            if win_clause:
                self.is_victorious = True
                break
            elif loss_clause:
                self.is_victorious = False
                break
            else:
                continue
        self.results(g)
        return g

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
        word whose length is exactly equal to 
        that of the mystery word
    attempts : list
        A list of all attempts made by the user 
        to guess the mystery word
    hits : list
        A list of all distinct letters contained
        within the mystery word that are guessed
        correctly by the user. The list may also 
        include the actual mystery word.
    misses : list
        A list of all distinct letters that are
        not contained within the mystery word that 
        are guessed by the user. The list may also 
        include whole words that are equal in 
        length to the mystery word.

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
        self.attempts = []
        self.hits = []
        self.misses = []

    def __str__(self):
        return self.value

    def __repr__(self):
        param_str = ", ".join(f"{k}='{v}'" for k,v in vars(self).items())
        return f"{self.__class__.__name__}({param_str})"

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
        response = None
        try:  # <-- recognize speech w/ Google Speech Recognition
            response = r.recognize_google(audio).lower().split(" ")[0]
        except sr.UnknownValueError:
            self.speak("I cannot recognize your speech.")
            return response
        except sr.RequestError:
            self.speak("I cannot contact the API.")
            return response
        else:
            if response == target:  # <-- prompt user to confirm guess if it hears target word
                self.speak(f"Did you say {response}? Say 'yes' or 'no' to confirm.")
                confirmation = self.listen("yes")
            return response if (response == target and confirmation == "yes") else response[0]

    def get_guess(self, target):
        base_prompt = "Enter a single letter in the target word, or enter the entire word itself: "
        while True:
            self.value = input(base_prompt).lower()
            if self.is_valid(target):
                return self.value.lower()

    def ask_guess(self, target):
        base_prompt = "Say a single letter in the target word, or say the entire word itself."
        alt_prompt = "It would seem that I may have difficulty understanding you clearly. As an alternative, please state a word from the phonetic alphabet and I will extract the first letter of the word I hear as your guess."
        err_count = 0
        while True:
            self.speak(base_prompt if err_count == 0 else alt_prompt)
            self.value = self.listen(target)
            if self.value == None:
                err_count += 1
                continue
            else:
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


class Outcome():
    """
    A class that represents the results
    for a game instance of 'Hangman'

    Attribute(s)
    ------------
    timestamp : datetime
        A timestamp denoting when the game ended
    is_victorious : bool
        Indicates whether or not a player
        won an instance of a game mode
    game_mode : str
        The name of the game mode instance
    mystery_word : str
        The target guess word for a game instance
    tries : int
        The total number of unique guesses made 
        by a user during a game instance
    guesses : list
        A list of all attempts made by the user 
        to guess the mystery word
    hits : list
        A list of all distinct letters contained
        within the mystery word that are guessed
        correctly by the user. The list may also 
        include the actual mystery word.
    misses : list
        A list of all distinct letters that are
        not contained within the mystery word that 
        are guessed by the user. The list may also 
        include whole words that are equal in 
        length to the mystery word.
    """
    def __init__(self, mode_obj, guess_obj):
        self.timestamp = datetime.datetime.now()
        self.is_victorious = mode_obj.is_victorious
        self.game_mode = mode_obj.name
        self.mystery_word = mode_obj._word
        self.guesses = guess_obj.attempts
        self.tries = len(self.guesses)
        self.hits = guess_obj.hits
        self.misses = guess_obj.misses

        if not self.game_mode in Game.victories.keys():
            Game.victories[self.game_mode] = []
        Game.victories[self.game_mode].append(self.is_victorious)

    def __str__(self):
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} | Victorious?: {str(self.is_victorious).ljust(5)} | Game Mode: {str(self.game_mode).title()}"

    def __repr__(self):
        param_str = ", ".join(f"{k}='{v}'" for k,v in vars(self).items())
        return f"{self.__class__.__name__}({param_str})"

