import random
import time
import datetime
import threading

import pyttsx3
import speech_recognition as sr


#========================================
# MENU CONFIGURATION
#========================================

class Option:
    """A class for the menu option of the Hangman application.

    Attributes
    ----------
    name : str
        The string identifier for an option.
    label : str
        The display name of an option.
    action : func
        A callback function to execute the selected option.

    Class Variables
    ---------------
    menu : list
        A list of all instantiated 'Option' objects.
    """
    menu = []

    def __init__(self, name:str, label:str, action):
        """Constructor method for the 'Option' class.

        Parameters
        ----------
        name : str
            The string identifer for an option.
        label : str
            The display name of an option.
        action : func
            A callback function to execute the selected option.
        """
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
    """A class for a game instance of Hangman. A superclass of 'Mode'.

    Attributes
    ----------
    active_game : threading.Event
        An event object that manages the state of gameplay.
    time_limit : int, default = 180
        The maximum time, in seconds, allotted for a timed game.

    Class Variables
    ---------------
    history : list
        A list of instances for the 'Outcome' class.
    victories : dict
        A dictionary that maintains a tally for the number of wins per game mode played during a session.
    """
    history = []
    victories = {}

    def __init__(self, active_game=threading.Event(), time_limit=180):
        """Constructor method for the 'Game' class.

        Parameters
        ----------
        active_game : threading.Event
            An event object that manages state of gameplay.
        time_limit : int, default = 300
            The maximum time, in seconds, allotted for a timed game.
        """
        self.active_game = active_game
        self.time_limit = time_limit

    @staticmethod
    def speak(text):
        """A method that converts text to speech using the pyttsx3 library."""
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    @staticmethod
    def _communicate(condition:bool, f1, f2, text):
        """Determines how the computer communicates text to a user based on a logical condition.

        Parameters
        ----------
        condition : bool
            The condition that determines if `f1` or `f2` is called.
        f1, f2 : func
            A callback function used to communicate `text` to a user.
        text : str
            The message to be communicated to a user.

        """
        f1(text) if condition else  f2(text)

    @staticmethod
    def _praise():
        """A randomly-selected praise made by the computer during gameplay."""
        praise = ["Success!","Fantastic!","Awesome!","Phenomenal!"]
        return random.choice(praise)

    @staticmethod
    def _taunt():
        """A randomly-selected taunt made by the computer during gameplay."""
        taunt = ["Tough luck.","Bollocks, you can do better.","Are you serious?!","Aww... so close."]
        return random.choice(taunt)

    @staticmethod
    def _time_label(interval):
        """Returns a formatted string for the time assigned to `interval`."""
        mins, secs = divmod(interval, 60)
        return f"{mins:.0f} minutes and {secs:.0f} seconds"

    def _save_results(self, outcome_obj):
        """Appends an 'Outcome' object to the `history` class variable."""
        Game.history.append(outcome_obj)
    
    def _end_game(self):
        """Resets the flag of the `active_game` event to False."""
        print("Time's Up!")
        self.active_game.clear()

    def _create_timer(self):
        """Creates a 'Timer' thread object that triggers a callback function."""
        return threading.Timer(interval=self.time_limit, function=self._end_game)

    @classmethod
    def summary(cls):
        """A class method that displays a tally of wins for each game mode played during the current session."""
        print("Gameplay Summary".center(27))
        print(f"/{'-'*25}\\")
        for k, v in Game.victories.items():
            print(f"| {k.title().rjust(8)} Mode: {str(sum(v)).zfill(2)} of {str(len(v)).zfill(2)} |")
        print(f"\{'_'*25}/")
        print("\n\n")


class Mode(Game):
    """A subclass of 'Game' that represents a specific game mode of Hangman with custom gameplay parameters.

    Attributes
    ----------
    active_game : threading.Event
        An event object that manages the state of gameplay.
    is_victorious : bool, default = False
        Indicates whether a player won a game instance.
    time_limit : int, default = 180
        The maximum time (in seconds) allotted for a timed game.
    duration = float
        The duration of the gameplay measured in seconds.
    name : str, optional
        The string identifier for a game mode.
    label : str, optional
        The display name of a game mode.
    objective : str
        A description of the game mode objective.
    source : str or None, default = None
        The word source for a selected game mode.
    min_word_length : int, default = 8
        The minimum number of letters in a target word.
    has_timer : bool, default = False
        Indicates whether the game mode is timed.
    max_errors : int, default = 6
        The maximum number of errors a user is allowed to make before losing the game.
    word : str
        An unknown target word determined by the selected game mode.
    chars : set
        A set of all unique letters contained in `word`.
    blanks : list
        A list of placeholders (underscores) equal to the length of `word`.

    Class Variables
    ---------------
    all_modes : list
        A list of all instantiated 'Mode' objects.

    Methods
    -------
    get_word()
        Randomly selects a word from a source specified by the game mode, or a list of default words.
    play()
        A method that initializes an untimed game instance. Returns a 'Guess' object.
    timed_play()
        A method that initializes a timed game instance. Returns a 'Guess' object.
    results(guess_obj)
        A method that communicates the results of a game instance to the user.
    """
    all_modes = []

    def __init__(
        self, active_game=threading.Event(), is_victorious=False,
        time_limit=180, duration=0, 
        name=None, label=None, 
        objective=None, source=None, min_word_length=8, has_timer=False, max_errors=6):
        """Constructor method for the 'Mode' class.
            
        Attributes
        ----------
        active_game : threading.Event
            An event object that manages the state of gameplay.
        is_victorious : bool, default = False
            Indicates whether or not a player won a game instance.
        time_limit : int, default = 300
            The maximum time (in seconds) allotted for a timed game.
        duration = float
            The duration of the gameplay measured in seconds.
        name : str, optional
            The string identifer for a game mode.
        label : str, optional
            The display name of a game mode.
        objective : str
            A description of the game mode objective.
        source : str or None, default = None
            The word source for a selected game mode.
        min_word_length : int, default = 8
            The minimum number of letters in a target word.
        has_timer : bool, default = False
            Indicates whether or not the game mode is timed.
        max_errors : int, default = 6
            The maximum number of errors a user is allowed to make before losing the game.
        """
        super().__init__(active_game, time_limit)
        self.active_game = active_game
        self.is_victorious = is_victorious
        self.time_limit = time_limit
        self.duration = duration
        self.name = name
        self.label = label
        self.objective = objective
        self.source = source
        self.min_word_length = min_word_length
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

    def _contact_local_dicitionary(self):
        """This method makes a request from the built-in dictionary of a posix system and returns a response object.

        () -> response : dict
        
        Returns
        -------
        response['words'] : list
            A list of words if successful, None otherwise.
        response['successful'] : bool
            True if successful, False otherwise.
        response['error'] : str or None
            None if successful, a string error message otherwise.
        """
        response = {  # <-- response object
            'words': None,
            'successful': True,
            'error': None,
        }
        try:
            with open("/usr/share/dict/words", "r") as f:
                raw_list = f.read().split("\n")
                filtered_list = [word for word in raw_list if (len(word) >= self.min_word_length 
                and word[0].islower())]
        except:
            response["successful"] = False
            response["error"] = "I cannot reach the local system dictionary!"
        else:
            response["words"] = filtered_list
        finally:
            return response

    def _get_from_dictionary(self):
        """Returns a list of words if call to `contact_local_dictionary` was successful, None otherwise."""
        response = self._contact_local_dicitionary()
        return response['words']

    def _eavesdrop(self):
        """This method will convert speech recorded from a user's voice to text and return a response object.

        () -> response : dict

        Returns
        -------
        response['words'] : list
            A list of words if successful, None otherwise.
        response['successful'] : bool
            True if successful, False otherwise.
        response['error'] : str or None
            None if successful, a string error message otherwise.
        """
        r = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            # r.adjust_for_ambient_noise(source, 0.5)
            audio = r.listen(source)
        response = {
            'words': None,
            'successful': True,
            'error': None,
        }
        try:  # <-- recognize speech w/ Google Speech Recognition
            raw_word_list = r.recognize_google(audio).lower().split(" ")
            response['words'] = list(filter(lambda word: len(word) >= self.min_word_length, raw_word_list))
        except sr.UnknownValueError:
            response['successful'] = False
            response['error'] = "I cannot recognize your speech"
        except sr.RequestError:
            response['successful'] = False
            response['error'] = "I cannot contact the API"
        return response

    def _get_from_speech(self):
        """Returns a list of words if call to `eavesdrop` was successful, None otherwise."""
        while True:
            self.speak("Speak naturally and clearly for up to 30 seconds.")
            response = self._eavesdrop()
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
        """Randomly selects a word from a source specified by the game mode, or a list of default words."""
        DEFAULT_WORDS = [
            "resurrection", "osphresiology", "establishment","ridiculous","collection", "querimonious", "experimentation", "zealotry",
            "international", "vastation", "gemelliparous", "kyriolexy",
            "totalitarianism", "kaleidophone", "nephralgia",
            "juxtaposition", "decalescence", "calorifacient",
            "loquacious", "uniphonous", "abscissa",
            "differentiation", "kettlestitch", "halitosis",
            "logarithmic", "ultracrepidate", "biloquist",
            "quadrennium", "gawdelpus", "acritochromacy",
            "ethereal", "jactitation", "delaminate",
            "zwitterion", "oppignorate", "whippletree",
            "xenobiotic", "otorhinolaryngology", "eldritch",
            "transient", "oligarchy", "naturalism",
            "inconsequential", "grandisonant",
            "reverberate","capricious", "hematology",
            "whimsical", "xylography", "balatron",
            "disenfranchise", "neomorphic", "wrackful",]
        if self.source == "dictionary":
            words = self._get_from_dictionary()
        elif self.source == "speech":
            words = self._get_from_speech()
        if not self.source or (not words and self.source):
            words = DEFAULT_WORDS
        self._word = random.choice(words).lower()
        for char in self._word:
            self._chars.add(char)
        self._blanks = ["_" for _ in self._word]
        self._communicate(self.source == "speech", self.speak, print, f"The mystery word contains {len(self._word)} letters.")

    def _grade_guess(self, guess_obj):
        """Validates whether or not a user's guess equal to the target word or a letter contained within it.

        Parameters
        ----------
        guess_obj : Guess
            An instance of the 'Guess' class.

        Returns
        -------
        bool
            True if successful, False otherwise.
        """
        guess_obj.attempts.append(guess_obj.value)
        if len(guess_obj.value) == 1 and guess_obj._is_in_word(self._word):
            guess_obj.hits.append(guess_obj.value)
            return True
        elif len(guess_obj.value) == len(self._word) and guess_obj._is_word(self._word):
            guess_obj.hits.clear()
            guess_obj.hits.extend([char for char in guess_obj.value])
            return True
        else:
            guess_obj.misses.append(guess_obj.value)
            return False
        
    def _update_user(self, is_correct, is_speaking):
        """Communicates whether or not a user's guess was successful, and displays an updated game board to reflect the most recent attempt.

        Parameters
        ----------
        is_correct : bool
            Indicates whether or not the user's current guess is correct.
        is_speaking : bool
            Indicates whether or not the game speaks to the user.

        Returns
        -------
        None
        """
        if is_correct:
            self._communicate(is_speaking, self.speak, print, self._praise())
        else:
            self._communicate(is_speaking, self.speak, print, self._taunt())

    def play(self):
        """A method that initializes an untimed game instance. Returns a 'Guess' object."""
        start_time = time.time()
        g = Guess()
        does_game_speak = self.source == "speech"
        win_clause = False
        loss_clause = False
        for _ in range(2):
            print()
        g.show_board(
            g._hit_string(self._word, self._blanks), g.miss_string())
        self.active_game.set()
        while self.active_game.is_set() and not (win_clause or loss_clause):
            # Obtain and evaluate input from user
            while True:
                print()
                if does_game_speak:
                    g._ask_guess(self._word)
                else:
                    g._get_guess(self._word)
                if g._is_unique:
                    break
            if self.active_game.is_set():
                print()
                is_correct = self._grade_guess(g)
                self._update_user(is_correct, does_game_speak)
                for _ in range(2):
                    print()
                g.show_board(
                    g._hit_string(self._word, self._blanks), g.miss_string())

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
        self.duration = time.time() - start_time
        return g

    def timed_play(self):
        """A method that initializes an timed game instance. Returns a 'Guess' object."""
        does_game_speak = self.source == "speech"
        announce=f"You will have {self._time_label(self.time_limit)} to complete the game.\nGood luck.\n"
        t = self._create_timer()
        self._communicate(does_game_speak, self.speak, print, announce)
        t.start()
        guess_obj = self.play()
        if self.duration < self.time_limit:
            t.cancel()
        else:
            self.duration = self.time_limit
        return guess_obj

    def results(self, guess_obj):
        """A method that communicates the results of a game instance to the user.
        
        Parameters
        ----------
        guess_obj : Guess
            An instance of the 'Guess' class.

        Returns
        -------
        None
        """
        announce = dict(
            word=f"The correct word was `{self._word.upper()}`.",
            win=f"Congratulations. {'You finished...JUST IN TIME!!!' if self.has_timer else 'You won the game!'}\n",
            lose=f"You ran out of time! Tough luck.\n" if self.duration == self.time_limit else "Whomp whomp. You lose! Better luck next time.\n",
            duration=f"Game Duration: {self._time_label(self.duration)}",
        )
        print()
        does_game_speak = self.source == "speech"
        self._communicate(does_game_speak, self.speak, print, announce['word'])
        if self.is_victorious:
            self._communicate(does_game_speak, self.speak, print, announce['win'])
        else:
            self._communicate(does_game_speak, self.speak, print, announce['lose'])
        self._communicate(does_game_speak, self.speak, print, announce['duration'])
        self._save_results(Outcome(self, guess_obj))

# `Mode` instances
standard = Mode(
  name = "standard",
  label = "traditional game",
  objective = "Determine the mystery word before reaching the maximum number of errors.",
  source = "dictionary",
  min_word_length = 10)
timed = Mode(
  name = "timed",
  label = "just in time",
  objective = "Determine the mystery word before the time limit expires.",
  has_timer=True,)
speech = Mode(
  name = "speech",
  label = "listen up!",
  objective = "Determine a mystery word that is randomly chosen from an audio clip of the user's speech.",
  source = "speech",)


class Guess():
    """A class that represents a user's guesses of the target word generated by a game mode.

    Attributes
    ----------
    value : str
        The user's current guess.
    attempts : list
        A list of all unique guesses made by a user during a game instance.
    hits : list
        A list of all distinct letters contained within the target word that are guessed correctly by the user.
    misses : list
        A list of all distinct letters guessed by the user that are not contained within the target word. The list may also include whole words that are equal in length to the target word.

    Class Variables
    ---------------
    BODY : tuple
        The components of the 'Hangman' graphic displayed to a user.
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
        """Constructor method for the 'Guess' class.

        Parameters
        ----------
        The user's current guess.
        """
        self.value = value
        self.attempts = []
        self.hits = []
        self.misses = []

    def __str__(self):
        return self.value

    def __repr__(self):
        param_str = ", ".join(f"{k}='{v}'" for k,v in vars(self).items())
        return f"{self.__class__.__name__}({param_str})"

    def _is_valid(self, target):
        """Validates whether or not the user's guess is a single letter or a word of equal length to the target word.
        
        Parameters
        ----------
        target : str
            The target word for a game instance.

        Returns
        -------
        bool
            True if the condition is satisfied, False otherwise.
        """
        return str(self.value).isalpha() and (len(self.value) == 1 or len(self.value) == len(target))

    @property
    def _is_unique(self):
        """Indicates whether or not the user's guess is unique."""
        if self.value in self.misses or self.value in self.hits:
            print("You already used this guess.")
        return not(self.value in self.misses or self.value in self.hits)

    @staticmethod
    def _speak(text):
        """A method that converts text to speech using the pyttsx3 library."""
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    def listen(self, *args):
        """This method will convert speech from a user's voice to text and return a single letter, or a word if the response is equal to the target word.

        () -> response : str

        Returns
        -------
        response : str
            A string response of the user's current guess.
        """
        target = args[0] if args else None
        r = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            # r.adjust_for_ambient_noise(source, 0.5)
            audio = r.listen(source)
        response = None
        try:  # <-- recognize speech w/ Google Speech Recognition
            response = r.recognize_google(audio).lower().split(" ")[0]
        except sr.UnknownValueError:
            self._speak("I cannot recognize your speech.")
            return response
        except sr.RequestError:
            self._speak("I cannot contact the API.")
            return response
        else:
            return response if response == target else response[0]

    def _get_guess(self, target):
        """Prompts a user to input a guess of the target word.
        
        Parameters
        ----------
        target : str
            The target word for a game instance.

        Returns
        -------
        str
            The user's current guess.
        """
        base_prompt = "Enter a single letter in the target word, or enter the entire word itself: "
        while True:
            self.value = input(base_prompt).lower()
            if self._is_valid(target):
                return self.value.lower()

    def _ask_guess(self, target):
        """Prompts a user to say a guess of the target word.
        
        Parameters
        ----------
        target : str
            The target word for a game instance.

        Returns
        -------
        str
            The user's current guess.
        """
        base_prompt = "Say a single letter in the target word, or say the entire word itself."
        alt_prompt = "It would seem that I may have difficulty understanding you clearly. As an alternative, please state a word from the phonetic alphabet and I will extract the first letter of the word I hear as your guess."
        err_count = 0
        while True:
            self._speak(base_prompt if err_count == 0 else alt_prompt)
            self.value = self.listen(target)
            if self.value == None:
                err_count += 1
                continue
            else:
                return self.value.lower()

    def _is_in_word(self, word):
        """A method that indicates whether or not the guess is in the target word.
        
        Parameters
        ----------
        target : str
            The target word for a game instance.

        Returns
        -------
        bool
            True if successful, False otherwise.
        """
        return word.find(self.value) != -1

    def _is_word(self, word):
        """Returns a bool that indictates if the guess is the target word."""
        return self.value == word

    def _hit_string(self, target, placeholder):
        """A string display of placeholder text that is updated with correct guesses.
        
        Parameters
        ----------
        target : str
            The target word for a game instance.
        placeholder : list
            A list equal in length to the number of characters in the target word.

        Returns
        -------
        str
            Displays all correctly guessed letters in their corresponding location in the placeholder text.
        """
        for idx in range(len(target)):
            if len(self.value) == 1 and self.value == target[idx]:
                placeholder[idx] = self.value.upper()
            if self.value == target:
                placeholder = [char.upper() for char in self.value]
        return " ".join(placeholder)

    def miss_string(self):
        """Returns a string of all incorrect guesses."""
        return ", ".join(self.misses).upper()

    def show_board(self, h_string, m_string):
        """Displays an updated gameboard with all attempted guesses."""
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
    """A class that represents the results for a game instance of Hangman.

    Attributes
    ----------
    timestamp : datetime
        A timestamp denoting when the game instance ended.
    is_victorious : bool
        Indicates whether a player won the game instance.
    game_mode : str
        The string identifier for the game mode.
    target_word : str
        The target word for the game instance.
    tries : int
        The total number of unique guesses made by a user during the game instance.
    attempts : list
        A list of all unique guesses made by a user during the game instance.
    hits : list
        A list of all distinct letters contained within the target word that are guessed correctly by the user.
    misses : list
        A list of all distinct letters guessed by the user that are not contained within the target word. The list may also include whole words that are equal in length to the target word.
    """
    def __init__(self, mode_obj, guess_obj):
        """Constructor method for the 'Outcome' class.

        Parameters
        ----------
        mode_obj : Mode
            An instance of the 'Mode' class.
        guess_obj : Guess
            An instance of the 'Guess' class.
        """
        self.timestamp = datetime.datetime.now()
        self.is_victorious = mode_obj.is_victorious
        self.game_mode = mode_obj.name
        self.target_word = mode_obj._word
        self.attempts = guess_obj.attempts
        self.tries = len(self.attempts)
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



if __name__ == '__main__':
    pass
