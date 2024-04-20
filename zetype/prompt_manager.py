from dataclasses import dataclass


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


class PromptManager:
    """
    Manages a typing prompt for a word per minute (WPM) test application.

    Attributes:
        prompt (str): The prompt string for input processing.
        cursor_index (int): The current cursor position within the prompt.
        total_typed (int): The total number of characters typed.
        total_typed_correct (int): The total number of characters typed correctly.
        error_log (list[InputError]): A list of InputError instances tracking typing errors.
    """

    def __init__(self, prompt: str) -> None:
        """
        Initialize the PromptManager instance.

        Args:
            prompt (str): The prompt string for input processing.
        """
        self.prompt = prompt
        self.cursor_index = 0
        self.total_typed, self.total_typed_correct = 0, 0
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

    @property
    def total_typed_incorrect(self) -> int:
        """
        Get the total number of incorrectly typed characters.

        Returns:
            int: The count of characters typed incorrectly.
        """
        return self.total_typed - self.total_typed_correct

    @property
    def typing_accuracy(self) -> float:
        """
        Calculate the typing accuracy as a percentage.

        Returns:
            float: The typing accuracy percentage.
        """
        if self.total_typed == 0:
            return 100.0  # Default to 100% accuracy if no characters are typed
        return (self.total_typed_correct / self.total_typed) * 100

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

    def process_input(self, char: str) -> bool:
        """
        Process input character and update typing statistics.

        Args:
            char (str): The input character to process.

        Returns:
            bool: True if the input character matches the expected character at the cursor index, otherwise False.
        """
        self._check_str_is_char(char)

        is_incorrect = (self.current_character != char)
        if is_incorrect:
            error = InputError(
                index=self.cursor_index,
                expected_char=self.current_character,
                received_char=char,
            )
            self.error_log.append(error)

        self.cursor_index += 1
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
