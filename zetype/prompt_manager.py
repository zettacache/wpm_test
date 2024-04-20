"""Module responsible for the back-end logic of the typing test."""

from dataclasses import dataclass
from time import time
from typing import Optional

from zetype.calculations import minutes_since


@dataclass
class InputError:
    """
    Represents an error that occurs during input processing.

    Attributes:
        index (int): The index where the error occurred.
        expected_char (str): The expected character at the error index.
        received_char (str): The character that was received instead.
    """
    index: int
    expected_char: str
    received_char: str


@dataclass
class TypingStats:
    """
    Tracks the overall statistics of a `PromptManager`.

    Attributes:
        _start_time (int):  The time which `words_per_minute` will be calculated from
        total_typed (int):  The total amount of characters typed, correctly or incorrectly.
        total_errors (int): The total amount of characters typed incorrectly.
    """
    _start_time = time()
    total_typed = 0
    total_errors = 0

    @property
    def total_correct(self) -> int:
        """
        Get the total number of correctly typed characters.

        Returns:
            int: The count of characters typed correctly.
        """
        return self.total_typed - self.total_errors

    @property
    def typing_accuracy(self) -> Optional[float]:
        """
        Calculate the typing accuracy as a percentage.

        Returns:
            float | None: Percentage accuracy (0-100). Returns `None` if no characters are counted.
        """
        if self.total_typed == 0:
            return None

        return (self.total_correct / self.total_typed) * 100

    @property
    def words_per_minute(self) -> Optional[float]:
        """
        Calculates the average typed words per minute.

        Returns:
            float | None: Average words per minute. Returns `None` if no characters are counted.
        """
        if self.total_typed == 0:
            return None

        # The average amount of characters in an english word.
        average_chars_per_word = 4.7

        words_typed = self.total_typed / average_chars_per_word
        return words_typed / minutes_since(self._start_time)

    def update_start_time(self, start_time=time()) -> None:
        """
        Updates `self._start_time` to the provided time.

        Args:
            start_time (float): New start time in seconds (defaults to time of method call).
        """
        self._start_time = start_time

    def count_character(self, is_correct: bool = True) -> None:
        """
        Increments the total character counters.

        Args:
            is_correct (bool): Tracks character as correct or incorrect (defaults to True).
        """
        self.total_typed += 1
        if not is_correct:
            self.total_errors += 1


class PromptManager:
    """
    Manages a typing prompt for a word per minute (WPM) test application.

    Attributes:
        prompt (str): The prompt string for input processing.
        cursor_index (int): The current cursor position within the prompt.
        error_log (list[InputError]): A list of InputError instances tracking typing errors.
    """

    def __init__(self, prompt: str) -> None:
        """
        Initialize the PromptManager instance.

        Args:
            prompt (str): The prompt string for input processing.
        """
        self.prompt, self.cursor_index = prompt, 0

        self.stats = TypingStats()
        self.error_log: list[InputError] = []

    @property
    def current_character(self) -> str:
        """
        Get the current character from the prompt string based on the cursor index.

        Returns:
            str: The current character in the prompt.
        """
        return self.prompt[self.cursor_index]

    @property
    def prompt_until_cursor(self) -> str:
        """
        Get the portion of the prompt string from the beginning up to the cursor index.

        Returns:
            str: The substring of the prompt up to the cursor position.
        """
        return self.prompt[:self.cursor_index]

    @staticmethod
    def _check_str_is_char(char: str) -> None:
        """
        Check if the input string is a single character.

        Args:
            char (str): The input string to check.

        Raises:
            ValueError: If the input string length is not 1.
        """
        if len(char) != 1:
            raise ValueError(f"Expected a single character, but received '{char}'")

    def _check_index_in_bounds(self, index: int) -> None:
        """
        Check if the provided index is within the bounds of `self.prompt`.

        Args:
            index (int): The index to check.

        Raises:
            IndexError: If the index is not within bounds.
        """
        if not self._is_index_in_bounds(index):
            raise IndexError(f"Index {index} is out of bounds.")

    def _is_index_in_bounds(self, index: int) -> bool:
        """
        Check if the provided index is within the bounds of `self.prompt`.

        Args:
            index (int): The index to check.

        Returns:
            bool: Whether the index is within bounds or not.
        """
        return 0 <= index < len(self.prompt)

    def _check_relative_index_in_bounds(self, index: int) -> None:
        """
        Check if the provided index is within the bounds of `self.prompt` relative to the cursor.

        Args:
            index (int): The distance from cursor to check.

        Raises:
            IndexError: If the index is not within bounds.
        """
        if not self._is_relative_index_in_bounds(index):
            raise IndexError(f"Index {self.cursor_index + index} is out of bounds.")

    def _is_relative_index_in_bounds(self, index: int) -> bool:
        """
        Check if the provided index is within the bounds of `self.prompt` relative to the cursor.

        Args:
            index (int): The distance from cursor to check.

        Returns:
            bool: Whether the index is within bounds or not.
        """
        return 0 <= (self.cursor_index + index) < len(self.prompt)

    def _move_cursor(self, amount: int) -> None:
        """
        Moves the cursor index by a provided amount.

        Args:
            amount (int): The amount to move the cursor.

        Raises:
            IndexError: If the new index is not within bounds.
        """
        self._check_relative_index_in_bounds(amount)
        self.cursor_index += amount

    def process_input(self, char: str) -> bool:
        """
        Process input character and update typing statistics.

        Args:
            char (str): The input character to process.

        Returns:
            bool: If character is correct or not.

        Raises:
            ValueError: If `len(char) != 1`
        """
        self._check_str_is_char(char)

        # Add index to `self.error_log` if the character does not match.
        if is_incorrect := self.current_character != char:
            error = InputError(
                index=self.cursor_index,
                expected_char=self.current_character,
                received_char=char,
            )
            self.error_log.append(error)
        is_correct = not is_incorrect

        # Moves cursor forward if within bounds
        if self._is_relative_index_in_bounds(1):
            self._move_cursor(1)

        self.stats.count_character(is_correct=is_correct)

        return is_correct

    def revert_last_input(self) -> None:
        """
        Reverts last input including char, cursor, and errors.

        Raises:
            IndexError: If there is no previous input to revert.
        """
        if not self._is_relative_index_in_bounds(-1):
            return

        self._move_cursor(-1)
        if (len(self.error_log) > 0) and (self.error_log[-1].index == self.cursor_index):
            self.error_log.pop()

    def segment_prompt(self, max_length: int, start_pos: int = 0):
        """
        Generates segmented strings from `self.prompt` of size `max_length` or shorter

        Args:
            max_length (int): The maximum length of a segment
            start_pos (int): The starting position within the prompt to segment (default 0)

        Yields:
            int: Segment iteration
            str: Segmented string from `self.prompt`
            list[InputError]: List of errors contained within the segment with relative indexes.
        """
        errors = self.error_log[:]
        row = 0
        while start_pos < len(self.prompt):
            # Create a segment at `start_pos` of size `max_length`
            segment = self.prompt[start_pos:][:max_length]

            # Check if segment contains a space, if it does, trim the string to that point.
            if (" " in segment) and (index := segment.rindex(" ")):
                segment = segment[:index]

            # Resolve the segmented indices of errors from `self.error_log`
            segment_errors = []
            for index, error in enumerate(errors):
                if start_pos <= error.index < (start_pos + len(segment)):
                    error.index -= start_pos
                    segment_errors.append(errors.pop(index))

            # Update `start_pos` for next segment
            start_pos += len(segment)

            # Yield string segment, and `InputError`s within string segment.
            yield row, segment, segment_errors
            row += 1
