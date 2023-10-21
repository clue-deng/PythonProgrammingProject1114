# Author: Yingtong Deng
# Guessing Game
# Date due: 2020-11-06


####### DO NOT EDIT CODE BELOW (changing MAX_MISSES is ok) ########
import random
import sys

MAX_MISSES = 5
BORDER_LENGTH = 30
SINGLE_CHAR_LENGTH = 1


def blank_chars(word):
    """Returns a list of underscore characters with the same length as word.

    :param word: target word as a string
    :return: a list of underscore characters ('_')

    >>> blank_chars("happiness")
    ['_', '_', '_', '_', '_', '_', '_', '_', '_']
    """
    word_list = []
    for i in range(len(word)):
        underscore = "_"
        word_list.append(underscore)

    return word_list


def space_chars(chars):
    """Returns a string with the characters in chars list separated by spaces.

    :param chars: a list of characters
    :return: a string containing characters in chars with intervening spaces

    >>> space_chars(['h', '_', 'p', 'p', '_', 'n', '_', '_', '_'])
    'h _ p p _ n _ _ _'
    """
    chars = " ".join(chars)
    return chars


def get_guess():
    """Prompts the user for a guess to check for the game's current word. When the user
    enters input other than a single character, the function prompts the user again
    for a guess. Only when the user enters a single character will the prompt for
    a guess stop being displayed. The function returns the single-character guess
    entered by the user.

    :return guess: a single character guessed by user
    """

    guess = input("Guess:\t")
    while len(guess) != SINGLE_CHAR_LENGTH or not guess.isalpha():
        guess = input("Guess:\t")
    guess = guess.lower()
    return guess


def check_guess(word, guess):
    """Returns a list of positions where guess is present in word.
    An empty list should be returned when guess is not a single
    character or when guess is not present in word.


    :param word: target word as a string
    :param guess: a single character guessed by user
    :return positions: list of integer positions
    """
    positions = []
    start = 0
    if guess in word and len(guess) == SINGLE_CHAR_LENGTH:
        num_guess = word.count(guess)
        for i in range(num_guess):
            guess_index = word.find(guess, start, len(word))
            positions.append(guess_index)
            start = guess_index + SINGLE_CHAR_LENGTH

    return positions


def update_chars(chars, guess, positions):
    """Updates the list of characters, chars, so that the characters
    at the index values in the positions list are updated to the
    character guess.


    :param chars: a list of characters
    :param guess: a single character guessed by user
    :param positions: list of integer positions
    :return: None
    """
    for num in positions:
        chars[num] = guess


def add_to_misses(misses, guess):
    """Adds the character guess to the misses list.

    :param misses: list of guesses not present in target word
    :param guess: a single character guessed by user
    :return: None
    """
    misses.append(guess)


def update_state(chars, misses, guess, positions):
    """Updates the state of the game based on user's guess. Calls the function update_chars() when
    the positions list is not empty to reveal the indices where the character guess is present. Calls the
    function add_to_misses() when the positions list is empty to add guess to the misses list.

    :param chars: a list of characters
    :param misses: list of guesses not present in target word
    :param guess: a single character guessed by user
    :param positions: list of integer positions
    :return: None
    """

    if positions != []:
        update_chars(chars, guess, positions)
    else:
        add_to_misses(misses, guess)


def is_round_complete(chars, misses):
    """Indicates whether or not a round has ended. This function returns True
    when the user has successfully guessed the target word or exceeds the
    number of allowed misses. Otherwise, the function returns False,
    indicating that the round is not complete. A message revealing the
    user's success or failure guessing the target word is output by this
    function when the round is complete.


    :param chars: a list of characters
    :param misses: list of guesses not present in target word
    :return status: True when round is finished, False otherwise
    """

    chars_string = "".join(chars)
    if "_" not in chars_string:
        print("\nYOU GOT IT!")
        return True
    elif len(misses) > MAX_MISSES:
        print("\nSORRY! NO GUESSES LEFT.")
        return True
    else:
        return False


def read_words(filepath):
    """Opens a file of word located at filepath, reads the file of words line by line,
    and adds each word from the file to a list. The list is returned by the
    function

    :param filepath: path to input file of words (one per line)
    :return word_list: list of strings contained in input file
    """
    file = open(filepath, "r")
    words_list = file.readlines()
    words_string = "".join(words_list)
    words_list = words_string.split("\n")
    file.close()

    return words_list


def get_word(words):
    """Selects a single word randomly from words list and returns it.

    :param words: list of strings
    :return word: string from words list
    """
    word_index = random.randrange(0, len(words))
    word = words[word_index]
    return word


def is_game_complete():
    """Prompts the user with "Play again (Y/N)?". The question is repeated
    until the user enters a valid response (one of Y/y/N/n). The function
    returns False if the user enters 'Y' or 'y' and returns True if the user
    enters 'N' or 'n'.

    :return response: boolean representing game completion status
    """
    another_round = input("Play again (Y/N)? ")
    while another_round not in ("Y", "N", "y", "n"):
        another_round = input("Play again (Y/N)? ")
    if another_round == "Y" or another_round == "y":
        return False
    if another_round == "N" or another_round == "n":
        return True


def run_guessing_game(words_filepath):
    """Controls running The Guessing Game. This includes parsing
    the words file and executing multiple rounds of the game.

    :param words_filepath: the location of the file of words for the game
    :return: None
    """
    try:
        words_list = read_words(words_filepath)
    except FileNotFoundError:
        print("The provided file location is not valid. Please enter a valid path to a file.")
        return False
    print("Welcome to The Guessing Game!")
    another_game = None
    while another_game != True:
        targeted_word = get_word(words_list)
        word_list = blank_chars(targeted_word)
        misses_list = []
        round_status = None
        while round_status != True:
            display_game_state(word_list, misses_list)
            guess = get_guess()
            positions = check_guess(targeted_word, guess)
            update_state(word_list, misses_list, guess, positions)
            round_status = is_round_complete(word_list, misses_list)
        display_game_state(targeted_word, misses_list)
        another_game = is_game_complete()
    if another_game == True:
        print("\nGoodbye.")


def display_game_state(chars, misses):
    """
    Displays the current state of the game: the list of characters to display
    and the list of misses.
    """

    print()
    print('=' * BORDER_LENGTH)
    print()

    print("Word:\t{}\n".format(space_chars(chars)))
    print("Misses:\t{}\n".format("".join(misses)))



def main():
    filepath = sys.argv[-1]

    # call run_guessing_game() with filepath as argument and remove pass below
    run_guessing_game(filepath)


if __name__ == '__main__':
    main()