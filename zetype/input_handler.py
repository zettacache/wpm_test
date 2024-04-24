"""Module that handles input logic from `app.py`."""

from dataclasses import dataclass
from enum import Enum, auto

from zetype.prompt_manager import PromptManager, InputResponse


class InputAction(Enum):
    """Possible actions returned to the application that need to be handled."""
    NONE = auto()
    EXIT_PROGRAM = auto()
    RESIZE = auto()
    UNDO = auto()
    PROCESSED_INPUT = auto()
    COMPLETE = auto()


@dataclass
class InputCode:
    """List of common meta-key input codes."""
    BLANK = -1
    ABORT = 3  # KeyboardInterrupt
    ESCAPE = 27
    BACKSPACE = 8
    DELETE = 127
    RESIZE = 410


class InputHandler:  # pylint: disable=too-few-public-methods
    """Used as an input-processing middle-man between `app.py` and `prompt_manager.py`"""

    def __init__(self, prompt: PromptManager) -> None:
        self.prompt = prompt

    def process_getch(self, user_input: int) -> InputAction:
        """
        Determines app behavior from the return of getch.

        Args:
            user_input (int): Input code (should be from getch)

        Returns:
            InputAction: A brief descriptor of how `user_input` was processed
        """

        if user_input == InputCode.BLANK:
            return InputAction.NONE

        match user_input:
            case InputCode.ABORT | InputCode.ESCAPE:
                return InputAction.EXIT_PROGRAM
            case InputCode.RESIZE:
                return InputAction.RESIZE
            case InputCode.BACKSPACE | InputCode.DELETE:
                self.prompt.revert_last_input()
                return InputAction.UNDO
            case _:
                char = chr(user_input)
                response = self.prompt.process_input(char)
                return (InputAction.COMPLETE
                        if response == InputResponse.COMPLETE else InputAction.PROCESSED_INPUT)
