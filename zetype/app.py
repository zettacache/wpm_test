"""Module responsible for the application runtime."""

import curses
from time import time
from zetype.colors import Colors
from zetype.prompt_manager import PromptManager
from zetype.input_handler import InputHandler, InputAction


class App:
    """Main application class for terminal-based interaction"""
    # pylint: disable=too-many-instance-attributes

    def __init__(self, window: curses.window):
        """Initialize the application with a curses window.

        Args:
            window (curses.window): The window to use for input and output.
        """
        self.window = window
        self.is_running = False
        self.is_finished = False
        self.app_start_time = time()
        self.prompt = PromptManager("Hello GitHub, this is zetype! "
                                    "I am a project created to showcase my python skills.")
        self.input = InputHandler(self.prompt)
        self.final_words_per_minute = -1.0
        self.final_typing_accuracy = -1.0

    def initialize(self) -> None:
        """Initialize the curses environment."""
        curses.noecho()  # Disable echoing user input
        curses.curs_set(0)  # Hide the cursor
        curses.raw()  # Enter raw input mode
        Colors.initialize()
        self.window.timeout(100)  # Set timeout for blocking input
        self.window.nodelay(True)  # Enable non-blocking input
        self.window.keypad(True)  # Enable arrow keys
        self.window.bkgdset(curses.color_pair(Colors.PRIMARY))

    def _process_input(self) -> None:
        """Process user keyboard input."""
        user_input = self.window.getch()

        input_action = self.input.process_getch(user_input)
        if self.is_finished and input_action != InputAction.NONE:
            self.stop()
        else:
            if input_action == InputAction.EXIT_PROGRAM:
                self.stop()
            elif input_action == InputAction.COMPLETE:
                self._finalize()

    def _render(self) -> None:
        """Render the current state of the application."""
        self.window.clear()
        if self.is_finished:
            self._render_finished()
        else:
            self._render_prompt()
            self._render_typed_characters()
            self._render_incorrect_characters()
            self._render_cursor()
            self._render_stats()

    def _render_finished(self) -> None:
        self.window.addstr(0, 0, "You have completed the prompt with the following stats:")
        self.window.addstr(1, 0, f"WPM: {int(self.final_words_per_minute)}")
        self.window.addstr(2, 0, f"Accuracy: {int(self.final_typing_accuracy)}%")
        self.window.addstr(3, 0, "Press any key to exit...")

    def _render_prompt(self) -> None:
        self.window.addstr(0, 0, self.prompt.prompt, curses.A_DIM)

    def _render_typed_characters(self) -> None:
        self.window.addstr(0, 0, self.prompt.prompt_until_cursor)

    def _render_incorrect_characters(self) -> None:
        for error in self.prompt.error_log:
            self.window.addstr(
                0,
                error.index,
                error.expected_char,
                curses.color_pair(Colors.WRONG) | curses.A_UNDERLINE
            )

    def _render_cursor(self) -> None:
        self.window.addstr(
            0,
            self.prompt.cursor_index,
            self.prompt.current_character,
            curses.color_pair(Colors.PRIMARY_INVERTED)
        )

    def _render_stats(self) -> None:
        wpm = (
            f" WPM: {int(wpm_float)} "
            if (wpm_float := self.prompt.stats.words_per_minute)
            else " TYPE TO START "
        )
        accuracy = (
            f" ACC: {int(accuracy_float)}% "
            if (accuracy_float := self.prompt.stats.typing_accuracy) is not None
            else " TYPE TO START "
        )

        # WPM text
        self.window.addstr(4, 0, wpm, curses.color_pair(Colors.PRIMARY_INVERTED))
        # Accuracy text
        self.window.addstr(5, 0, accuracy, curses.color_pair(Colors.PRIMARY_INVERTED))

    def _finalize(self):
        self.is_finished = True
        self.final_words_per_minute = self.prompt.stats.words_per_minute or -1
        self.final_typing_accuracy = self.prompt.stats.typing_accuracy or -1

    def run(self) -> None:
        """Run the main application loop."""
        self.is_running = True
        while self.is_running:
            self._process_input()
            self._render()

    def stop(self) -> None:
        """Stop the application."""
        self.is_running = False
        curses.curs_set(1)  # Unhide the cursor
