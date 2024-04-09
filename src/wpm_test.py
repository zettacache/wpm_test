from math import ceil
from random import choice


class WpmTester:
    def __init__(self, word_list: list[str], amount_of_words: int, words_per_line=10):
        self.amount_of_words = amount_of_words
        self.current_line = 0

        # Generate a word list of len == `amount_of_words`
        self.word_list = [choice(word_list) for _ in range(amount_of_words)]
        # Find the amount of lines needed
        line_amount = ceil(len(self.word_list) / words_per_line)
        # Chop the word list into sub-lists of len == `amount_of_words`
        self.word_list = [self.word_list[n * words_per_line: (n + 1) * words_per_line] for n in range(line_amount)]

    def start(self, lines_shown=3):
        return
