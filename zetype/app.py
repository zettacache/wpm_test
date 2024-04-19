import curses
from time import time
from zetype import minutes_since, get_accuracy, get_words_typed, TypingManager, Colors, Key


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
        self.prompt = TypingManager("Hello GitHub, this is zetype! I am a passion project created.")

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

        match user_input:
            case Key.ABORT | Key.ESCAPE:
                self.stop()
            case Key.RESIZE:
                raise NotImplemented
            case Key.BACKSPACE | Key.DELETE:
                self.prompt.undo_previous_input()
            case Key.BLANK:
                return
            case _:
                is_char_correct = self.prompt.process_input(chr(user_input))
                self.char_total += 1
                if is_char_correct:
                    self.char_correct += 1

    def _render(self) -> None:
        """Render the current state of the application."""
        self.window.clear()
        self._render_prompt()
        self._render_typed_characters()
        self._render_incorrect_characters()
        self._render_cursor()
        self._render_stats()

    def _render_prompt(self) -> None:
        self.window.addstr(0, 0, self.prompt.prompt_text, curses.A_DIM)

    def _render_typed_characters(self) -> None:
        self.window.addstr(0, 0, self.prompt.get_substringed())

    def _render_incorrect_characters(self) -> None:
        for index, char in self.prompt.get_wrong_characters():
            self.window.addstr(
                0,
                index,
                char,
                curses.color_pair(Colors.WRONG) | curses.A_UNDERLINE
            )

    def _render_cursor(self) -> None:
        self.window.addstr(
            0,
            self.prompt.current_index,
            self.prompt.current_character,
            curses.color_pair(Colors.PRIMARY_INVERTED)
        )

    def _render_stats(self) -> None:
        self.window.addstr(
            4,
            0,
            f" WPM: {int(self.wpm)} ",
            curses.color_pair(Colors.PRIMARY_INVERTED)
        )
        self.window.addstr(
            5,
            0,
            f" ACC: {int(self.char_accuracy)}% ",
            curses.color_pair(Colors.PRIMARY_INVERTED)
        )

    def _calculate_stats(self) -> None:
        """Calculate any necessary statistics."""
        self.wpm = get_words_typed(self.char_total) / minutes_since(self.app_start_time)
        self.char_accuracy = get_accuracy(self.char_correct, self.char_total)

    def run(self) -> None:
        """Run the main application loop."""
        self.is_running = True
        while self.is_running and not self.prompt.done:
            self._process_input()
            self._calculate_stats()
            self._render()

    def stop(self) -> None:
        """Stop the application."""
        self.is_running = False
