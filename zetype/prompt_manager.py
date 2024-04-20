from dataclasses import dataclass
from time import time

from zetype import minutes_since


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
    def typing_accuracy(self) -> float:
        """
        Calculate the typing accuracy as a percentage.

        TODO: Make return optional when `self.total_typed == 0`

        Returns:
            float: The typing accuracy percentage (0-100).
        """
        if self.total_typed == 0:
            return 100.0  # Default to 100% accuracy if no characters are typed
        return (self.total_correct / self.total_typed) * 100

    @property
    def words_per_minute(self) -> float:
        """
        Calculates the average typed words per minute.

        NOTE: Possibly, revisit this to more accurately track wpm instead of average characters per word.
        Although that could introduce a prompt bias based on length of words given.

        Returns:
            float: Average words per minute since `self._start_time`
        """
        words_typed = self.total_typed / 4.7  # 4.7 is the average amount of characters in an english word.
        return words_typed / minutes_since(self._start_time)

    def update_start_time(self, start_time=time()) -> None:
        """
        Updates `self._start_time` to the provided time.

        Args:
            start_time (float): The new start time in seconds (defaults to time of calling the method).
        """
        self._start_time = start_time

    def count_character(self, is_correct: bool = True) -> None:
        """
        Increments the total character counters.

        Args:
            is_correct (bool): Whether the character should be counted as correct or as an error (defaults to True).
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

    def _check_relative_index_in_bounds(self, index: int) -> None:
        """
        Check if the provided index is within the bounds of `self.prompt` relative to the cursor.

        Args:
            index (int): The distance from cursor to check.

        Raises:
            IndexError: If the index is not within bounds.
        """
        if not (0 <= (index + self.cursor_index) <= len(self.prompt)):
            raise IndexError(f"Index {index} is out of bounds.")

    def _is_relative_index_in_bounds(self, index: int) -> bool:
        """
        Check if the provided index is within the bounds of `self.prompt` relative to the cursor.

        Args:
            index (int): The distance from cursor to check.

        Returns:
            bool: Whether the index is within bounds or not.
        """
        return 0 <= (index + self.cursor_index) <= len(self.prompt)

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
            bool: True if the input character matches the expected character at the cursor index, otherwise False.

        Raises:
            ValueError: If `len(char) != 1`
        """
        self._check_str_is_char(char)

        # Add index to `self.error_log` if the character does not match.
        if is_incorrect := (self.current_character != char):
            error = InputError(
                index=self.cursor_index,
                expected_char=self.current_character,
                received_char=char,
            )
            self.error_log.append(error)

        # Update stats and cursor
        self.stats.count_character(is_correct=(not is_incorrect))
        self._move_cursor(1)

        return not is_incorrect

    def revert_last_input(self) -> None:
        """
        Revert the cursor position to the previous character and remove the last input error from the log.

        Raises:
            IndexError: If there is no previous input to revert.
        """
        if self.cursor_index == 0:
            raise IndexError("No previous input to revert.")

        self.cursor_index -= 1
        if len(self.error_log) > 0 and (self.error_log[-1].index == self.cursor_index):
            self.error_log.pop()
