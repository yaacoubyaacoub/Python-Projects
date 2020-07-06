# Problem Set 4B
# Name: Yaacoub Yaacoub
# Time Spent: x:xx

import string


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


def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story_PS4.txt", "r")
    story = str(f.read())
    f.close()
    return story


### END HELPER CODE ###

WORDLIST_FILENAME = 'words_PS4.txt'


class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object

        text (string): the message's text

        a Message object has two attributes:
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

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.

        shift (integer): the amount by which to shift every letter of the
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to
                 another letter (string).
        '''
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        cipher_to_letter = {}
        for letter in string.ascii_letters:
            if letter in lowercase:
                new_letter_index = lowercase.index(letter) + shift
                if new_letter_index >= 26:
                    new_letter_index = new_letter_index - 26
                cipher_to_letter[letter] = lowercase[new_letter_index]
            elif letter in uppercase:
                new_letter_index = (uppercase.index(letter) - 26) + shift
                if new_letter_index >= 26:
                    new_letter_index = new_letter_index - 26
                cipher_to_letter[letter] = uppercase[new_letter_index]
        return cipher_to_letter

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift

        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        shifted_letters = self.build_shift_dict(shift)

        the_message = self.get_message_text()
        encrypted_message = ""
        for char in the_message:
            if char in shifted_letters.keys():
                encrypted_message = encrypted_message + shifted_letters[char]
            else:
                encrypted_message = encrypted_message + char
        return encrypted_message


class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object

        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        Message.__init__(self, text)
        self.shift = shift
        self.encryption_dict = Message.build_shift_dict(self, shift)
        self.message_text_encrypted = Message.apply_shift(self, shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class

        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class

        Returns: a COPY of self.encryption_dict
        '''
        return self.encryption_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class

        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other
        attributes determined by shift.

        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        self.encryption_dict = Message.build_shift_dict(self, shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object

        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create
        the maximum number of valid words, you may choose any of those shifts
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        message = self.get_message_text()
        valid_words = self.get_valid_words()
        message_dict = {}
        validity = {}
        for i in range(26):
            new_message = ""
            for letter in message:
                if letter in lowercase:
                    new_letter_index = lowercase.index(letter) - i
                    if new_letter_index < 0:
                        new_letter_index = new_letter_index + 26
                    new_message = new_message + str(lowercase[new_letter_index])
                elif letter in uppercase:
                    new_letter_index = uppercase.index(letter) - i
                    if new_letter_index < 0:
                        new_letter_index = new_letter_index + 26
                    new_message = new_message + str(uppercase[new_letter_index])
                else:
                    new_message = new_message + str(letter)
            message_dict[i] = new_message
            words = new_message.split()
            valid = 0
            for word in words:
                if is_word(valid_words, word):
                    valid += 1
            validity[i] = valid
        is_valid = 0
        the_message = "No valid message"
        shift = 0
        for j in validity.keys():
            if validity[j] >= is_valid and validity[j] != 0:
                is_valid = validity[j]
                the_message = message_dict[j]
                shift = int(j)
                if shift != 0:
                    shift = 26 - shift
        return (shift, the_message)


if __name__ == '__main__':
    # Example test case (PlaintextMessage)
    plaintext = PlaintextMessage('hello', 2)
    print('Expected Output: jgnnq')
    print('Actual Output:', plaintext.get_message_text_encrypted())

    # Example test case (CiphertextMessage)
    ciphertext = CiphertextMessage('jgnnq')
    print('Expected Output:', (24, 'hello'))
    print('Actual Output:', ciphertext.decrypt_message())

    story = CiphertextMessage(get_story_string())
    decrypted_story = story.decrypt_message()
    print("Encrypted story:", get_story_string())
    print("Decrypted story:", decrypted_story[1])
