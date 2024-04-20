"""Ensures proper functionality of `prompt_manager.py`."""

import unittest
from zetype.prompt_manager import PromptManager, InputError


class TestPromptManager(unittest.TestCase):
    """Tests PromptManager class."""

    def test_process_input_correct(self):
        """Tests that correct user-input is processed as correct."""
        prompt = "Hello, world!"
        manager = PromptManager(prompt)

        self.assertTrue(manager.process_input('H'))
        self.assertEqual(manager.cursor_index, 1)
        self.assertEqual(manager.stats.total_typed, 1)
        self.assertEqual(manager.stats.total_errors, 0)

        self.assertTrue(manager.process_input('e'))
        self.assertEqual(manager.cursor_index, 2)
        self.assertEqual(manager.stats.total_typed, 2)
        self.assertEqual(manager.stats.total_errors, 0)

    def test_process_input_incorrect(self):
        """Tests that incorrect user-input is processed as incorrect."""
        prompt = "Hello, world!"
        manager = PromptManager(prompt)

        self.assertFalse(manager.process_input('h'))
        self.assertEqual(manager.cursor_index, 1)
        self.assertEqual(manager.stats.total_typed, 1)
        self.assertEqual(manager.stats.total_errors, 1)
        self.assertEqual(len(manager.error_log), 1)

        error = manager.error_log[0]
        self.assertIsInstance(error, InputError)
        self.assertEqual(error.index, 0)
        self.assertEqual(error.expected_char, 'H')
        self.assertEqual(error.received_char, 'h')

    def test_revert_last_input(self):
        """Tests that reverting last input is processed correctly."""
        prompt = "Hello, world!"
        manager = PromptManager(prompt)

        manager.process_input('H')
        manager.process_input('e')
        manager.process_input('l')
        manager.process_input('p')

        self.assertEqual(manager.cursor_index, 4)
        self.assertEqual(manager.stats.total_typed, 4)
        self.assertEqual(manager.stats.total_errors, 1)

        manager.revert_last_input()
        self.assertEqual(manager.cursor_index, 3)
        self.assertEqual(manager.stats.total_typed, 4)
        self.assertEqual(manager.stats.total_errors, 1)


if __name__ == '__main__':
    unittest.main()
