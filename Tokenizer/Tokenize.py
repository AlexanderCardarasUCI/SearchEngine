import re
from nltk.stem import PorterStemmer
from autocorrect import Speller

ps = PorterStemmer()
spell = Speller()

def stem_word(token):
    return ps.stem(token)


# O(n) where n is the number of characters in the text file
def tokenize(text, spellcheck=False):
    """ open text file and create a list of all words """

    # deliminate by special characters inspiration from
    # https://stackoverflow.com/questions/1276764/stripping-everything-but-alphanumeric-chars-from-a-string-in-python
    my_tokens = re.split("[^a-zA-Z0-9_]+", text)

    # array for storing tokens
    all_tokens = []

    # add all tokens to the tokens list
    for token in my_tokens:

        # in some cases r.split will return an empty string as a token
        # one case is if two delimiting characters are next to each other
        if len(token) > 0:

            if spellcheck:
                token = spell.autocorrect_word(token)

            # change text to lowercase
            token = token.lower()
            token = stem_word(token)
            all_tokens.append(token)

    return all_tokens

def remove_duplicates(tokens):
    new_tokens = {}

    for token in tokens:
        if token not in new_tokens:
            new_tokens[token] = 0

    return new_tokens.keys()

# O(n^2) where n is the number of unique roman character strings in the text file
def compute_word_frequencies(my_tokens):
    """ counts the number of appearances of ea idf have an effect on ranking ch token. returns Map<token, count> """

    frequencies = {}

    for token in my_tokens:
        if token in frequencies:
            frequencies[token] += 1
        else:
            frequencies[token] = 1

    return frequencies


def compute_token_analytics(my_tokens):

    frequencies = {}
    positions = {}

    for index, token in enumerate(my_tokens):
        # Frequencies
        if token in frequencies:
            frequencies[token] += 1
        else:
            frequencies[token] = 1

        # Positions
        if token in positions:
            positions[token].append(index)
        else:
            positions[token] = [index]

    return frequencies, positions
