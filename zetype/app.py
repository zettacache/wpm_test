import curses
from time import time
from zetype import PromptManager, Colors, InputHandler, InputAction


class App:
    """Main application class for terminal-based interaction"""

    def __init__(self, window: curses.window):
        """Initialize the application with a curses window.

        Args:
            window (curses.window): The window to use for input and output.
        """
        self.window = window
        self.is_running = False
        self.app_start_time = time()
        self.prompt = PromptManager("Hello GitHub, this is zetype! "
                                    "I am a passion project created as a means to showcase my python skills.")
        self.input = InputHandler(self.prompt)

        self.wpm: float = 0
        # TODO: Turn character tracking properties into a more organized structure
        self.char_correct: int = 0
        self.char_total: int = 0
        self.char_accuracy = 0

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
        if input_action == InputAction.EXIT_PROGRAM:
            self.stop()

    def _render(self) -> None:
        """Render the current state of the application."""
        self.window.clear()
        self._render_prompt()
        self._render_typed_characters()
        self._render_incorrect_characters()
        self._render_cursor()
        self._render_stats()

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
        if wpm := self.prompt.stats.words_per_minute:
            wpm_text = f" WPM: {int(wpm)} "
        else:
            wpm_text = " TYPE TO START "
        self.window.addstr(
            4,
            0,
            wpm_text,
            curses.color_pair(Colors.PRIMARY_INVERTED)
        )

        if accuracy := self.prompt.stats.typing_accuracy:
            accuracy_text = f" ACC: {int(accuracy)}% "
        else:
            accuracy_text = " TYPE TO START "
        self.window.addstr(
            5,
            0,
            accuracy_text,
            curses.color_pair(Colors.PRIMARY_INVERTED)
        )

    def run(self) -> None:
        """Run the main application loop."""
        self.is_running = True
        while self.is_running:
            self._process_input()
            self._render()

    def stop(self) -> None:
        """Stop the application."""
        self.is_running = False
