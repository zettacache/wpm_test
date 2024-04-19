class TypingManager:
    def __init__(self, prompt_text: str):
        """Initialize TypingManager with a prompt text."""
        self.prompt_text = prompt_text
        self.current_index = 0
        self.mistake_indexes = []
        self.done = False

    @property
    def current_character(self) -> str:
        """Get the current character from the prompt text."""
        return self.prompt_text[self.current_index]

    def process_input(self, character: str) -> bool:
        """Process a character input by the user."""
        correct = True
        if self.current_character != character:
            self.mistake_indexes.append(self.current_index)
            correct = False
        if self.current_index != len(self.prompt_text) - 1:
            self.current_index += 1
        else:
            self.done = True
        return correct

    def undo_previous_input(self):
        """Undo the last character input if possible."""
        if self.current_index > 0:
            if self.current_index - 1 in self.mistake_indexes:
                self.mistake_indexes.remove(self.current_index - 1)
            self.current_index -= 1

    def get_wrong_characters(self):
        """Generator function to yield wrong indexes with corresponding characters."""
        for index in self.mistake_indexes:
            yield index, self.prompt_text[index]

    def get_substringed(self):
        return self.prompt_text[:self.current_index]
