from dataclasses import dataclass
from enum import Enum, auto

from zetype import PromptManager


class InputAction(Enum):
    NONE = auto()
    EXIT_PROGRAM = auto()
    RESIZE = auto()
    UNDO = auto()
    PROCESS_CHARACTER = auto()


@dataclass
class InputCode:
    BLANK = -1
    ABORT = 3  # KeyboardInterrupt
    ESCAPE = 27
    BACKSPACE = 8
    DELETE = 127
    RESIZE = 410


class InputHandler:
    def __init__(self, prompt: PromptManager) -> None:
        self.prompt = prompt

    def process_getch(self, user_input: int) -> InputAction:
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
                self.prompt.process_input(char)
                return InputAction.PROCESS_CHARACTER
