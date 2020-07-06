# Problem Set 2, hangman.py
# Name: Yaacoub Yaacoub
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words_PS2.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    number_of_letters_guessed = 0
    for letters in secret_word:
        for lett in letters_guessed:
            if lett == letters:
                number_of_letters_guessed += 1
    if number_of_letters_guessed == len(secret_word):
        return True
    else:
        return False


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    word = ""
    for letters in secret_word:
        counter = 0
        for lett in letters_guessed:
            if lett == letters:
                counter += 1
        if counter == 0:
            word = str(word) + "_"
        else:
            word = str(word) + str(letters)
    return word


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    remaining_letters = ""
    lettres = string.ascii_lowercase
    for letter in lettres:
        counter = 0
        for lett in letters_guessed:
            if lett == letter:
                counter += 1
        if counter == 0:
            remaining_letters = str(remaining_letters) + str(letter)
    return remaining_letters


def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    Follows the other limitations detailed in the problem write-up.
    '''

    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is", len(secret_word), "letters long")
    print("---------------------------------------------------------------")

    warnings = 3
    guesses = 6
    print("You have", warnings,
          "warnings left:\n  (You can only use lowercase alphabet, and any other character typed or if a lowercase letter is typed twice will result a warning)\n  (if you get 3 warnings, one guess will be lost)")
    print("You have", guesses, "guesses")
    print("Available letters:", string.ascii_lowercase)
    letters_guessed = []

    while guesses > 0:
        guess = input("Please guess a letter: ")
        while len(guess) != 1 or guess not in string.ascii_lowercase:
            if warnings == 0:
                warnings = 3
                guesses -= 1
            else:
                warnings -= 1
            print("Warning!")
            print("You have to provide one lowercase letter only!")
            print("----------------------------------------------------------")
            print("Available letters:", get_available_letters(letters_guessed))
            print("You have", warnings, "warnings left")
            print("You have", guesses, "guesses left")
            guess = input("Please guess a letter: ")

        while guess in letters_guessed:
            if warnings == 0:
                warnings = 3
                guesses -= 1
            else:
                warnings -= 1
            print("Warning!")
            print("You already chose this letter, one warning will be lost")
            print("You have to provide one lowercase letter only!")
            print("----------------------------------------------------------")
            print("Available letters:", get_available_letters(letters_guessed))
            print("You have", warnings, "warnings left")
            print("You have", guesses, "guesses left")
            guess = input("Please guess a letter: ")

        letters_guessed.append(guess)
        if guess in secret_word:
            print("Good guess!", get_guessed_word(secret_word, letters_guessed))
        elif guess in "aeoui":
            guesses = guesses - 2
            print("Oops! that letter is not in my word:", get_guessed_word(secret_word, letters_guessed))
        else:
            guesses -= 1
            print("Oops! that letter is not in my word:", get_guessed_word(secret_word, letters_guessed))
        print("----------------------------------------------------------")
        print("You have", warnings, "warnings left")
        print("You have", guesses, "guesses left")
        print("Available letters:", get_available_letters(letters_guessed))
        if is_word_guessed(secret_word, letters_guessed):
            print("The secret word was", secret_word, "!")
            print("Congratulation, you won!")
            number_of_unique_letters = 0
            for a in secret_word:
                counter = -1
                for b in secret_word:
                    if b == a:
                        counter += 1
                if counter == 0:
                    number_of_unique_letters += 1
            total_score = guesses * number_of_unique_letters
            print("Your total score for this game is", total_score)
            break
    if not is_word_guessed(secret_word, letters_guessed):
        print("Sorry, you ran out of guesses. the word was:", secret_word)


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
# (hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    '''
    flag = 0
    if len(my_word) == len(other_word):
        for letter in my_word:
            if letter != "_":
                if other_word[my_word.index(letter)] != letter:
                    flag = 0
                    break
            flag = 1
    if flag == 0:
        return False
    elif flag == 1:
        return True


def show_possible_matches(my_word, letters_guessed):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    list = []
    for words in wordlist:
        flag = 0
        if match_with_gaps(my_word, words):
            for index in range(0, len(my_word)):
                if words[index] in letters_guessed:
                    if my_word[index] == "_":
                        flag = 1
                if my_word[index] != "_":
                    if my_word[index] != words[index]:
                        flag = 1
            if flag == 0:
                list.append(words)
    if len(list) == 0:
        return "No matches found"
    else:
        return list


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word.

    Follows the other limitations detailed in the problem write-up.
    '''

    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is", len(secret_word), "letters long")
    print("---------------------------------------------------------------")

    warnings = 3
    guesses = 6
    hint = 2
    print("You have", warnings,
          "warnings left:\n  (You can only use lowercase alphabet, and any other character typed or if a lowercase "
          + "letter is typed twice will result a warning)\n  (if you get 3 warnings, one guess will be lost)")
    print("You have", guesses, "guesses")
    print("You have", hint, "hints")
    print("Available letters:", string.ascii_lowercase)
    letters_guessed = []

    while guesses > 0:
        guess = input("Please guess a letter: ")

        while (len(guess) != 1 or guess not in string.ascii_lowercase) and guesses != 0:
            if guess == "*":
                break
            if warnings == 0:
                warnings = 3
                guesses -= 1
                if guesses == 0:
                    break
            else:
                warnings -= 1
            print("Warning!")
            print("You have to provide one lowercase letter only!")
            print("----------------------------------------------------------")
            print("Available letters:", get_available_letters(letters_guessed))
            print("You have", warnings, "warnings left")
            print("You have", guesses, "guesses left")
            print("You have", hint, "hints left")
            guess = input("Please guess a letter: ")

        while guess in letters_guessed and guesses != 0:
            if warnings == 0:
                warnings = 3
                guesses -= 1
                if guesses == 0:
                    break
            else:
                warnings -= 1
            print("Warning!")
            print("You already chose this letter, one warning will be lost")
            print("You have to provide one lowercase letter only!")
            print("----------------------------------------------------------")
            print("Available letters:", get_available_letters(letters_guessed))
            print("You have", warnings, "warnings left")
            print("You have", guesses, "guesses left")
            print("You have", hint, "hints left")
            guess = input("Please guess a letter: ")

        if guess == "*":
            if hint > 0:
                hint -= 1
                hints_list = show_possible_matches(get_guessed_word(secret_word, letters_guessed), letters_guessed)
                print("Possible words matches are:", hints_list)
                print("You have", hint, "hints left")
            else:
                print("No hints left, last hints are:", hints_list)

        elif guesses != 0:
            letters_guessed.append(guess)
            if guess in secret_word:
                print("Good guess!", get_guessed_word(secret_word, letters_guessed))
            elif guess in "aeoui":
                guesses = guesses - 2
                print("Oops! that letter is not in my word:", get_guessed_word(secret_word, letters_guessed))
            else:
                guesses -= 1
                print("Oops! that letter is not in my word:", get_guessed_word(secret_word, letters_guessed))
        print("----------------------------------------------------------")
        print("You have", warnings, "warnings left")
        print("You have", guesses, "guesses left")
        print("You have", hint, "hints left")
        print("Available letters:", get_available_letters(letters_guessed))
        if is_word_guessed(secret_word, letters_guessed):
            print("----------------------------------------------------------")
            print("----------------------------------------------------------")
            print("The secret word was", secret_word, "!")
            print("Congratulation, you won!")
            number_of_unique_letters = 0
            for a in secret_word:
                counter = -1
                for b in secret_word:
                    if b == a:
                        counter += 1
                if counter == 0:
                    number_of_unique_letters += 1
            total_score = guesses * number_of_unique_letters
            print("Your total score for this game is", total_score)
            break
    if not is_word_guessed(secret_word, letters_guessed):
        print("----------------------------------------------------------")
        print("----------------------------------------------------------")
        print("Sorry, you ran out of guesses. the word was:", secret_word)


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.

    # secret_word =choose_word(wordlist)
    # hangman(secret_word)

    # To test part 3 re-comment out the above lines and
    # uncomment the following two lines.

    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
