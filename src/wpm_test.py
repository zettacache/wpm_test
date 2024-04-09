from math import ceil, floor
from random import choice
from enum import Enum
import time

import curses
from curses import wrapper


class TextStyle(Enum):
    DECAYED = 1
    DECAYED_WRONG = 2
    DECAYED_WRONG_SPACE = 3
    CURRENT = 4
    CURRENT_WRONG = 5
    CURRENT_WRONG_SPACE = 6
    COMPLETED = 7
    COMPLETED_WRONG_SPACE = 8
    FUTURE = 9
    RED = 10
    GREEN = 11
    STAT = 12


def setup_curses():
    curses.init_pair(TextStyle.DECAYED.value, 236, 235)  # DECAYED
    curses.init_pair(TextStyle.DECAYED_WRONG.value, 95, 235)  # DECAYED_WRONG
    curses.init_pair(TextStyle.DECAYED_WRONG_SPACE.value, 95, 95)  # DECAYED_WRONG_SPACE
    curses.init_pair(TextStyle.CURRENT.value, 15, 239)  # CURRENT
    curses.init_pair(TextStyle.CURRENT_WRONG.value, 203, 239)  # CURRENT_WRONG
    curses.init_pair(TextStyle.CURRENT_WRONG_SPACE.value, 131, 131)  # CURRENT_WRONG_SPACE
    curses.init_pair(TextStyle.COMPLETED.value, 247, 235)  # COMPLETED
    curses.init_pair(TextStyle.COMPLETED_WRONG_SPACE.value, 203, 203)  # COMPLETED_WRONG_SPACE
    curses.init_pair(TextStyle.FUTURE.value, 238, 235)  # FUTURE
    curses.init_pair(TextStyle.RED.value, 203, 235)  # RED
    curses.init_pair(TextStyle.GREEN.value, 119, 235)  # GREEN
    curses.init_pair(TextStyle.STAT.value, 240, 235)  # STAT

    curses.noecho()
    curses.curs_set(0)


def words_to_string(words: list[str]) -> str:
    return " ".join(words)


def find_longest_line(words: list[list[str]]) -> int:
    biggest = 0
    for line in words:
        line = words_to_string(line)
        if len(line) > biggest:
            biggest = len(line)
    return biggest


def get_total_char_len(words: list[list[str]]) -> int:
    total = 0
    for line in words:
        line = words_to_string(line)
        total += len(line)
    return total


def get_wpm(start_time: float, total_chars: int) -> int:
    words_typed = total_chars / 4.7
    seconds_passed = time.time() - start_time
    minutes_passed = seconds_passed / 60
    return ceil(words_typed / minutes_passed)



def clamp(n, n_min, n_max):
    return sorted((n_min, n, n_max))[1]


class WpmTester:
    def __init__(self, word_list: list[str], amount_of_words: int, words_per_line=7):
        self.amount_of_words = amount_of_words
        self.current_line = ""
        self.current_line_pos = 0
        self.current_char = ""
        self.current_char_pos = 0
        self.total_right = 0
        self.total_wrong = 0
        self.total_char_pos = 0
        self.start_time = 0

        # Generate a word list of len == `amount_of_words`
        self.word_list = [choice(word_list) for _ in range(amount_of_words)]
        # Find the amount of lines needed
        line_amount = ceil(len(self.word_list) / words_per_line)
        # Chop the word list into sub-lists of len == `amount_of_words`
        self.word_list = [self.word_list[n * words_per_line: (n + 1) * words_per_line] for n in range(line_amount)]

        self.wrong_characters = [[] for _ in range(line_amount)]
        self.total_char = get_total_char_len(self.word_list)
        self.longest_line = find_longest_line(self.word_list)

    def start(self, lines_shown=3):
        self.start_time = time.time()
        def render(count: int, screen: curses.window):
            screen.clear()
            curr_line, line_pos = self.current_line, self.current_line_pos
            curr_char, char_pos = self.current_char, self.current_char_pos

            def print_previous_line(amount: int, ln: int, col: int = 0):
                # Safe-check to ensure we are within bounds.
                if line_pos - amount < 0:
                    return

                previous_line = words_to_string(self.word_list[line_pos - amount])
                screen.addstr(ln, col, previous_line, curses.color_pair(TextStyle.DECAYED.value))

                for i in self.wrong_characters[line_pos - amount]:
                    char = previous_line[i]
                    screen.addstr(ln, col + i, char, curses.color_pair(TextStyle.DECAYED_WRONG_SPACE.value
                                                                       if char == " " else TextStyle.DECAYED_WRONG.value))

            def print_current_line(ln: int, col: int = 0):
                # All characters
                screen.addstr(ln, col, self.current_line, curses.color_pair(TextStyle.FUTURE.value))
                # Completed characters
                screen.addstr(ln, col, self.current_line[0:char_pos], curses.color_pair(TextStyle.COMPLETED.value))
                # Cursor
                screen.addstr(ln, col + char_pos, curr_char, curses.color_pair(TextStyle.CURRENT.value))
                # Wrong characters
                for i in self.wrong_characters[line_pos]:
                    char = self.current_line[i]
                    screen.addstr(ln, col + i, char, curses.color_pair(TextStyle.COMPLETED_WRONG_SPACE.value
                                                                       if char == " " else TextStyle.RED.value))
                    if i == char_pos:
                        screen.addstr(ln, col + i, char, curses.color_pair(TextStyle.CURRENT_WRONG_SPACE.value
                                                                           if char == " " else TextStyle.CURRENT_WRONG.value))

            def print_future_line(amount: int, ln: int, col: int = 0):
                # Safe-check to ensure we are within bounds.
                if line_pos + amount >= len(self.word_list):
                    return

                future_line = words_to_string(self.word_list[line_pos + amount])
                screen.addstr(ln, col, future_line, curses.color_pair(TextStyle.FUTURE.value))

            ln_offset, col_offset = 6, 10

            screen.addstr(ln_offset - 2, col_offset, "zettacache/wpm_test", curses.color_pair(TextStyle.FUTURE.value))
            print_previous_line(1, ln_offset + 1, col_offset)
            print_current_line(ln_offset + 2, col_offset)
            print_future_line(1, ln_offset + 3, col_offset)
            print_future_line(2, ln_offset + 4, col_offset)
            print_future_line(3, ln_offset + 5, col_offset)
            print_future_line(4, ln_offset + 6, col_offset)

            total = self.total_right + self.total_wrong
            if total > 0:
                accuracy = f"Accuracy: {(self.total_right / total * 100):.2f}%"
                screen.addstr(ln_offset + 10, col_offset + self.longest_line - len(accuracy), accuracy, curses.color_pair(TextStyle.STAT.value))
            screen.addstr(ln_offset + 10, col_offset, f"WPM: {get_wpm(self.start_time, self.total_right + self.total_wrong)}",
                              curses.color_pair(TextStyle.STAT.value))
            timed_passed = floor(time.time() - self.start_time)
            timed_passed_minutes = str(floor(timed_passed / 60))
            timed_passed_seconds = str(floor(timed_passed % 60)).zfill(2)
            timed_passed = f"{timed_passed_minutes}:{timed_passed_seconds}"
            screen.addstr(ln_offset + 11, col_offset + self.longest_line - len(timed_passed), timed_passed,
                          curses.color_pair(TextStyle.STAT.value))
            screen.addstr(ln_offset + 11, col_offset, f"Characters: {self.total_char_pos}/{self.total_char}",
                          curses.color_pair(TextStyle.STAT.value))

            screen.refresh()

        def main(screen: curses.window):
            setup_curses()
            screen.bkgd(' ', curses.color_pair(TextStyle.FUTURE.value) | curses.A_BOLD)
            count = 0
            while True:
                self.current_line = " ".join(self.word_list[self.current_line_pos]) + " "
                self.current_char = self.current_line[self.current_char_pos]
                render(count, screen)
                count += 1
                char = screen.getch()
                if char == 27:
                    break
                if char == 8 or char == 127 or char == curses.KEY_BACKSPACE:
                    self.total_char_pos -= 1
                    if self.current_char_pos in self.wrong_characters[self.current_line_pos]:
                        self.wrong_characters[self.current_line_pos].remove(self.current_char_pos)
                    self.current_char_pos -= 1
                    if self.current_char_pos < 0 < self.current_line_pos:
                        self.current_line_pos = clamp(self.current_line_pos - 1, 0, len(self.word_list))
                        self.current_char_pos = len(" ".join(self.word_list[self.current_line_pos]))
                    elif self.current_char_pos < 0:
                        self.current_char_pos = 0
                    continue
                self.total_char_pos += 1
                if chr(char) == self.current_char:
                    self.total_right += 1
                    if self.current_char_pos in self.wrong_characters[self.current_line_pos]:
                        self.wrong_characters[self.current_line_pos].remove(self.current_char_pos)
                    self.current_char_pos += 1
                    if self.current_char_pos >= len(self.current_line):
                        self.current_line_pos += 1
                        self.current_char_pos = 0
                else:
                    self.total_wrong += 1
                    if self.current_char_pos not in self.wrong_characters[self.current_line_pos]:
                        self.wrong_characters[self.current_line_pos].append(self.current_char_pos)
                    self.current_char_pos += 1
                    if self.current_char_pos >= len(self.current_line):
                        self.current_line_pos += 1
                        self.current_char_pos = 0

        wrapper(main)
