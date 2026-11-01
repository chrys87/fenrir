#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import string
import unittest
import importlib.util

sys.path.insert(0, os.path.abspath('src'))
from fenrirscreenreader.utils import word_utils

# Dynamically load the word echo commands
spec_type = importlib.util.spec_from_file_location(
    "word_echo_type",
    os.path.abspath("src/fenrirscreenreader/commands/onCursorChange/25000-word_echo_type.py")
)
word_echo_type_mod = importlib.util.module_from_spec(spec_type)
spec_type.loader.exec_module(word_echo_type_mod)

spec_nav = importlib.util.spec_from_file_location(
    "word_echo_navigation",
    os.path.abspath("src/fenrirscreenreader/commands/onCursorChange/60000-word_echo_navigation.py")
)
word_echo_nav_mod = importlib.util.module_from_spec(spec_nav)
spec_nav.loader.exec_module(word_echo_nav_mod)


class MockSettingsManager:
    def __init__(self, wordEcho=True):
        self.wordEcho = wordEcho

    def getSettingAsBool(self, section, key):
        if section == 'keyboard' and key == 'wordEcho':
            return self.wordEcho
        return True


class MockCursorManager:
    def __init__(self, horizontal=True, vertical=False):
        self.horizontal = horizontal
        self.vertical = vertical

    def isCursorHorizontalMove(self):
        return self.horizontal

    def isCursorVerticalMove(self):
        return self.vertical


class MockScreenManager:
    def __init__(self, delta=False):
        self._delta = delta

    def isDelta(self, ignoreSpace=False):
        return self._delta


class MockOutputManager:
    def __init__(self):
        self.spoken = []

    def presentText(self, text, interrupt=True, flush=False):
        self.spoken.append(text)


def create_mock_env(oldX, newX, y, lineText, wordEcho=True, horizontal=True, vertical=False, delta=False, outputManager=None):
    if outputManager is None:
        outputManager = MockOutputManager()
    env = {
        'runtime': {
            'settingsManager': MockSettingsManager(wordEcho=wordEcho),
            'cursorManager': MockCursorManager(horizontal=horizontal, vertical=vertical),
            'screenManager': MockScreenManager(delta=delta),
            'outputManager': outputManager,
        },
        'screen': {
            'oldCursor': {'x': oldX, 'y': y},
            'newCursor': {'x': newX, 'y': y},
            'newContentText': lineText,
        }
    }
    return env, outputManager


class TestWordUtils(unittest.TestCase):
    def test_get_current_word_basic(self):
        text = "hello world"
        x, y, w, eos, lb = word_utils.getCurrentWord(0, 0, text)
        self.assertEqual(w, "hello")
        self.assertEqual(x, 0)

        x, y, w, eos, lb = word_utils.getCurrentWord(4, 0, text)
        self.assertEqual(w, "hello")
        self.assertEqual(x, 0)

        x, y, w, eos, lb = word_utils.getCurrentWord(6, 0, text)
        self.assertEqual(w, "world")
        self.assertEqual(x, 6)

    def test_get_current_word_consecutive_spaces(self):
        text = "hello   world"
        # Cursor on space 1 (index 5)
        x, y, w, eos, lb = word_utils.getCurrentWord(5, 0, text)
        self.assertEqual(w, "hello")
        self.assertEqual(x, 0)

        # Cursor on space 2 (index 6)
        x, y, w, eos, lb = word_utils.getCurrentWord(6, 0, text)
        self.assertEqual(w, "hello")
        self.assertEqual(x, 0)

        # Cursor on space 3 (index 7)
        x, y, w, eos, lb = word_utils.getCurrentWord(7, 0, text)
        self.assertEqual(w, "hello")
        self.assertEqual(x, 0)

    def test_get_current_word_bounds(self):
        text = "hello"
        x, y, w, eos, lb = word_utils.getCurrentWord(10, 0, text)
        self.assertEqual(w, "hello")
        self.assertEqual(x, 0)

    def test_get_current_word_empty_and_whitespace(self):
        self.assertEqual(word_utils.getCurrentWord(0, 0, "")[2], "")
        self.assertEqual(word_utils.getCurrentWord(0, 0, "   ")[2], "")

    def test_get_prev_and_next_word(self):
        text = "first   second   third"
        x, y, w, eos, lb = word_utils.getNextWord(0, 0, text)
        self.assertEqual(w, "second")

        x, y, w, eos, lb = word_utils.getNextWord(x, 0, text)
        self.assertEqual(w, "third")

        x, y, w, eos, lb = word_utils.getPrevWord(x, 0, text)
        self.assertEqual(w, "second")


class TestWordEchoArrowNavigation(unittest.TestCase):
    def setUp(self):
        self.cmd = word_echo_type_mod.command()

    def test_arrow_over_two_spaces_after_word(self):
        # Issue #24: word echo triggers twice if there are two spaces after a word and you arrow over them
        text = "hello  world"
        output = MockOutputManager()
        # hello is indices 0..4, space 1 is 5, space 2 is 6, world is 7..11
        # Arrowing through the word
        for i in range(4):
            env, _ = create_mock_env(i, i + 1, 0, text, outputManager=output)
            self.cmd.initialize(env)
            self.cmd.run()
        self.assertEqual(output.spoken, [], "Should not echo while arrowing inside word")

        # Arrow from 'o' (4) to space 1 (5): crossing word boundary
        env, _ = create_mock_env(4, 5, 0, text, outputManager=output)
        self.cmd.env = env
        self.cmd.run()
        self.assertEqual(output.spoken, ["hello"], "Should echo 'hello' on entering first space")

        # Arrow from space 1 (5) to space 2 (6): consecutive whitespace, must NOT echo again!
        env, _ = create_mock_env(5, 6, 0, text, outputManager=output)
        self.cmd.env = env
        self.cmd.run()
        self.assertEqual(output.spoken, ["hello"], "Must NOT echo 'hello' second time on consecutive space")

        # Arrow from space 2 (6) to 'w' (7): enter next word
        env, _ = create_mock_env(6, 7, 0, text, outputManager=output)
        self.cmd.env = env
        self.cmd.run()
        self.assertEqual(output.spoken, ["hello"], "Should not echo on entering next word")

    def test_arrow_over_three_spaces(self):
        text = "hello   world"
        output = MockOutputManager()
        env, _ = create_mock_env(3, 4, 0, text, outputManager=output)
        self.cmd.initialize(env)
        self.cmd.run()

        # Space 1 (4 -> 5): triggers echo
        env, _ = create_mock_env(4, 5, 0, text, outputManager=output)
        self.cmd.env = env
        self.cmd.run()
        self.assertEqual(output.spoken, ["hello"])

        # Space 2 (5 -> 6): no echo
        env, _ = create_mock_env(5, 6, 0, text, outputManager=output)
        self.cmd.env = env
        self.cmd.run()
        self.assertEqual(output.spoken, ["hello"])

        # Space 3 (6 -> 7): no echo
        env, _ = create_mock_env(6, 7, 0, text, outputManager=output)
        self.cmd.env = env
        self.cmd.run()
        self.assertEqual(output.spoken, ["hello"])

    def test_arrow_back_and_forth(self):
        text = "cat  dog"
        output = MockOutputManager()
        # Initialize at 't' (2)
        env, _ = create_mock_env(1, 2, 0, text, outputManager=output)
        self.cmd.initialize(env)
        self.cmd.run()

        # Arrow to space 1 (2 -> 3)
        env, _ = create_mock_env(2, 3, 0, text, outputManager=output)
        self.cmd.env = env
        self.cmd.run()
        self.assertEqual(output.spoken, ["cat"])

        # Arrow to space 2 (3 -> 4)
        env, _ = create_mock_env(3, 4, 0, text, outputManager=output)
        self.cmd.env = env
        self.cmd.run()
        self.assertEqual(output.spoken, ["cat"])

        # Arrow back to space 1 (4 -> 3)
        env, _ = create_mock_env(4, 3, 0, text, outputManager=output)
        self.cmd.env = env
        self.cmd.run()
        self.assertEqual(output.spoken, ["cat"])

        # Arrow back onto 't' (3 -> 2): re-enters the word
        env, _ = create_mock_env(3, 2, 0, text, outputManager=output)
        self.cmd.env = env
        self.cmd.run()
        self.assertEqual(output.spoken, ["cat"])

        # Arrow to space 1 again (2 -> 3): word boundary crossed again, should echo
        env, _ = create_mock_env(2, 3, 0, text, outputManager=output)
        self.cmd.env = env
        self.cmd.run()
        self.assertEqual(output.spoken, ["cat", "cat"])

        # Arrow to space 2 again (3 -> 4): should not echo
        env, _ = create_mock_env(3, 4, 0, text, outputManager=output)
        self.cmd.env = env
        self.cmd.run()
        self.assertEqual(output.spoken, ["cat", "cat"])

    def test_multiple_words_with_double_spaces(self):
        text = "one  two  three  "
        output = MockOutputManager()
        env, _ = create_mock_env(0, 0, 0, text, outputManager=output)
        self.cmd.initialize(env)

        # Full arrow traversal
        for x in range(len(text) - 1):
            env, _ = create_mock_env(x, x + 1, 0, text, outputManager=output)
            self.cmd.env = env
            self.cmd.run()

        self.assertEqual(output.spoken, ["one", "two", "three"])


class TestWordEchoTyping(unittest.TestCase):
    def setUp(self):
        self.cmd = word_echo_type_mod.command()

    def test_typing_single_space(self):
        line = "hello " + " " * 50
        env, out = create_mock_env(5, 6, 0, line)
        self.cmd.initialize(env)
        self.cmd.run()
        self.assertEqual(out.spoken, ["hello"])

    def test_typing_consecutive_spaces_no_duplicate(self):
        line = "hello  " + " " * 50
        output = MockOutputManager()
        # Type first space: cursor moves 5 -> 6
        env, _ = create_mock_env(5, 6, 0, line, outputManager=output)
        self.cmd.initialize(env)
        self.cmd.run()
        self.assertEqual(output.spoken, ["hello"])

        # Type second space: cursor moves 6 -> 7
        env, _ = create_mock_env(6, 7, 0, line, outputManager=output)
        self.cmd.env = env
        self.cmd.run()
        self.assertEqual(output.spoken, ["hello"], "Typing second space should not duplicate word echo")

    def test_typing_letters_no_echo(self):
        line = "hello" + " " * 50
        output = MockOutputManager()
        # When typing letters, screen delta is present
        for i in range(len("hello")):
            env, _ = create_mock_env(i, i + 1, 0, line, delta=True, outputManager=output)
            self.cmd.initialize(env)
            self.cmd.run()
        self.assertEqual(output.spoken, [])

    def test_arrowing_inside_word_no_echo(self):
        line = "hello" + " " * 50
        output = MockOutputManager()
        # Moving within word characters: 0->1 ('e'), 1->2 ('l'), 2->3 ('l'), 3->4 ('o')
        for i in range(len("hello") - 1):
            env, _ = create_mock_env(i, i + 1, 0, line, delta=False, outputManager=output)
            self.cmd.initialize(env)
            self.cmd.run()
        self.assertEqual(output.spoken, [])


class TestWordEchoGuards(unittest.TestCase):
    def setUp(self):
        self.cmd = word_echo_type_mod.command()

    def test_word_echo_disabled(self):
        line = "hello  "
        env, out = create_mock_env(4, 5, 0, line, wordEcho=False)
        self.cmd.initialize(env)
        self.cmd.run()
        self.assertEqual(out.spoken, [])

    def test_vertical_cursor_move(self):
        line = "hello  "
        env, out = create_mock_env(4, 5, 0, line, vertical=True)
        self.cmd.initialize(env)
        self.cmd.run()
        self.assertEqual(out.spoken, [])

    def test_leading_spaces_no_echo(self):
        line = "   hello"
        output = MockOutputManager()
        for i in range(2):
            env, _ = create_mock_env(i, i + 1, 0, line, outputManager=output)
            self.cmd.initialize(env)
            self.cmd.run()
        self.assertEqual(output.spoken, [])


class TestWordEchoNavigationCommand(unittest.TestCase):
    def setUp(self):
        self.cmd = word_echo_nav_mod.command()

    def test_navigation_jump_to_word_start(self):
        line = "hello  world"
        # Jump from 0 to 7 (start of 'world')
        env, out = create_mock_env(0, 7, 0, line)
        self.cmd.initialize(env)
        self.cmd.run()
        self.assertEqual(out.spoken, ["world"])

    def test_navigation_jump_to_word_end(self):
        line = "hello  world"
        # Jump from 7 to 5 (end of 'hello')
        env, out = create_mock_env(7, 5, 0, line)
        self.cmd.initialize(env)
        self.cmd.run()
        self.assertEqual(out.spoken, ["hello"])

    def test_navigation_jump_disabled(self):
        line = "hello  world"
        env, out = create_mock_env(0, 7, 0, line, wordEcho=False)
        self.cmd.initialize(env)
        self.cmd.run()
        self.assertEqual(out.spoken, [])


if __name__ == '__main__':
    unittest.main()
