# Problem Set 4C
# Name: Yaacoub Yaacoub
# Time Spent: x:xx

import string
import random
from PS4a import get_permutations


### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing
    the list of words to load

    Returns: a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    '''

    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.

    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words_PS4.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'


class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object

        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class

        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.

        Returns: a COPY of self.valid_words
        '''
        return self.valid_words.copy()

    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)

        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled
        according to vowels_permutation. The first letter in vowels_permutation
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to
                 another letter (string).
        '''
        transpose_dict = {}
        for letter in string.ascii_letters:
            if letter in VOWELS_LOWER:
                transpose_dict[letter] = VOWELS_LOWER[vowels_permutation.index(letter)]
            elif letter in VOWELS_UPPER:
                transpose_dict[letter] = VOWELS_UPPER[vowels_permutation.index(letter.lower())]
            else:
                transpose_dict[letter] = letter
        return transpose_dict

    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary

        Returns: an encrypted version of the message text, based
        on the dictionary
        '''
        msg = self.get_message_text()
        encrypted_msg = ""
        for letter in msg:
            if letter in transpose_dict.keys():
                encrypted_msg = encrypted_msg + transpose_dict[letter]
            else:
                encrypted_msg = encrypted_msg + letter
        return encrypted_msg


class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        SubMessage.__init__(self, text)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message

        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.

        If no good permutations are found (i.e. no permutations result in
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message

        Hint: use your function from Part 4A
        '''
        permutations = get_permutations(VOWELS_LOWER)
        encrypted_msg = self.get_message_text()
        valid_words = self.get_valid_words()
        possible_message = {}
        possibility = 0
        validity = {}
        for v in permutations:
            possibility += 1
            decrypted_msg = ""
            for letter in encrypted_msg:
                if letter in VOWELS_LOWER:
                    decrypted_msg = decrypted_msg + VOWELS_LOWER[v.index(letter)]
                elif letter in VOWELS_UPPER:
                    decrypted_msg = decrypted_msg + VOWELS_UPPER[v.index(letter.lower())]
                else:
                    decrypted_msg = decrypted_msg + letter
            possible_message[possibility] = decrypted_msg
            words = decrypted_msg.split()
            valid = 0
            for word in words:
                if is_word(valid_words, word):
                    valid += 1
            validity[possibility] = valid
        is_valid = 0
        the_message = "No valid message"
        for j in validity.keys():
            if validity[j] >= is_valid and validity[j] != 0:
                is_valid = validity[j]
                the_message = possible_message[j]
        return the_message


if __name__ == '__main__':
    # Example test case
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())

    # Test 2
    message = SubMessage("Jack Florey is a mythical character created on the spur of a moment to help cover an "
                         + "insufficiently planned hack. He has been registered for classes at MIT twice before, "
                         + "but has reportedly never passed aclass. It has been the tradition of the residents of "
                         + "East Campus to become Jack Florey for a few nights each year to educate incoming students "
                         + "in the ways, means, and ethics of hacking.")
    permutation = random.choice(get_permutations(VOWELS_LOWER))
    enc_dict = message.build_transpose_dict(permutation)
    print("Permutation:", permutation)
    print("Original message: ", message.get_message_text())
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
