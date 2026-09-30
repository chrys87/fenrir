#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import unittest
from unittest import mock

# Ensure src is on sys.path
SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# Mock missing optional dependencies in test environment
if 'dbus' not in sys.modules:
    sys.modules['dbus'] = mock.MagicMock()
if 'pyte' not in sys.modules:
    pyte_mock = mock.MagicMock()
    pyte_mock.Screen = object
    sys.modules['pyte'] = pyte_mock

# Ensure gettext _ is present in builtins
import builtins
if not hasattr(builtins, '_'):
    builtins._ = lambda s: s

import termios
from fenrirscreenreader.commands.commands.copy_marked_to_clipboard import command as CopyCommand
from fenrirscreenreader.commands.commands.paste_clipboard import command as PasteCommand
from fenrirscreenreader.screenDriver.vcsaDriver import driver as VcsaDriver
from fenrirscreenreader.screenDriver.ptyDriver import driver as PtyDriver


class TestCopyMarkedToClipboard(unittest.TestCase):
    def setUp(self):
        self.cmd = CopyCommand()
        self.env = {
            'screen': {
                'newContentText': ''
            },
            'commandBuffer': {
                'Marks': {'1': None, '2': None}
            },
            'runtime': {
                'outputManager': mock.MagicMock(),
                'cursorManager': mock.MagicMock(),
                'memoryManager': mock.MagicMock(),
            }
        }
        self.cmd.initialize(self.env)

    def test_multiline_get_text_from_screen_strips_padding(self):
        # 80-column screen lines padded with spaces
        line1 = "first line".ljust(80)
        line2 = "second line".ljust(80)
        line3 = "third line".ljust(80)
        self.env['screen']['newContentText'] = f"{line1}\n{line2}\n{line3}"

        start_mark = {'x': 0, 'y': 0}
        end_mark = {'x': 9, 'y': 2}  # ends at 'third line'

        result = self.cmd.getTextFromScreen(start_mark, end_mark)
        expected = "first line\nsecond line\nthird line"
        self.assertEqual(result, expected)

    def test_multiline_selection_with_empty_lines(self):
        line1 = "heading".ljust(80)
        line2 = " ".ljust(80)  # blank line padded with 80 spaces
        line3 = "content".ljust(80)
        self.env['screen']['newContentText'] = f"{line1}\n{line2}\n{line3}"

        start_mark = {'x': 0, 'y': 0}
        end_mark = {'x': 6, 'y': 2}

        result = self.cmd.getTextFromScreen(start_mark, end_mark)
        expected = "heading\n\ncontent"
        self.assertEqual(result, expected)

    def test_multiline_selection_preserves_indentation(self):
        line1 = "def example():".ljust(80)
        line2 = "    val = 42".ljust(80)
        line3 = "    return val".ljust(80)
        self.env['screen']['newContentText'] = f"{line1}\n{line2}\n{line3}"

        start_mark = {'x': 0, 'y': 0}
        end_mark = {'x': 13, 'y': 2}

        result = self.cmd.getTextFromScreen(start_mark, end_mark)
        expected = "def example():\n    val = 42\n    return val"
        self.assertEqual(result, expected)

    def test_multiline_selection_with_start_offset(self):
        line1 = "prefix ignored; first line".ljust(80)
        line2 = "second line".ljust(80)
        self.env['screen']['newContentText'] = f"{line1}\n{line2}"

        start_mark = {'x': 16, 'y': 0}
        end_mark = {'x': 10, 'y': 1}

        result = self.cmd.getTextFromScreen(start_mark, end_mark)
        expected = "first line\nsecond line"
        self.assertEqual(result, expected)

    def test_singleline_selection_behavior_preserved(self):
        line = "hello   world".ljust(80)
        self.env['screen']['newContentText'] = line

        # Select 'hello'
        start_mark = {'x': 0, 'y': 0}
        end_mark = {'x': 4, 'y': 0}
        result = self.cmd.getTextFromScreen(start_mark, end_mark)
        self.assertEqual(result, "hello")

        # Select 'hello   ' with intentional trailing spaces on same line
        start_mark = {'x': 0, 'y': 0}
        end_mark = {'x': 7, 'y': 0}
        result = self.cmd.getTextFromScreen(start_mark, end_mark)
        self.assertEqual(result, "hello   ")

        # Select inside word
        start_mark = {'x': 8, 'y': 0}
        end_mark = {'x': 12, 'y': 0}
        result = self.cmd.getTextFromScreen(start_mark, end_mark)
        self.assertEqual(result, "world")

    def test_reversed_marks_handling(self):
        line1 = "line one".ljust(80)
        line2 = "line two".ljust(80)
        self.env['screen']['newContentText'] = f"{line1}\n{line2}"

        # Start mark at bottom, end mark at top
        start_mark = {'x': 7, 'y': 1}
        end_mark = {'x': 0, 'y': 0}

        result = self.cmd.getTextFromScreen(start_mark, end_mark)
        self.assertEqual(result, "line one\nline two")

    def test_empty_screen_or_none_marks(self):
        self.env['screen']['newContentText'] = ""
        self.assertEqual(self.cmd.getTextFromScreen({'x': 0, 'y': 0}, {'x': 0, 'y': 0}), "")
        self.assertEqual(self.cmd.getTextFromScreen(None, {'x': 0, 'y': 0}), "")
        self.assertEqual(self.cmd.getTextFromScreen({'x': 0, 'y': 0}, None), "")

    def test_copy_command_run_saves_to_clipboard_history(self):
        line1 = "alpha".ljust(80)
        line2 = "beta".ljust(80)
        self.env['screen']['newContentText'] = f"{line1}\n{line2}"
        self.env['commandBuffer']['Marks']['1'] = {'x': 0, 'y': 0}
        self.env['commandBuffer']['Marks']['2'] = {'x': 3, 'y': 1}

        self.cmd.run()

        self.env['runtime']['memoryManager'].addValueToFirstIndex.assert_called_once_with(
            'clipboardHistory', "alpha\nbeta"
        )
        self.env['runtime']['cursorManager'].clearMarks.assert_called_once()


class TestPasteClipboard(unittest.TestCase):
    def setUp(self):
        self.cmd = PasteCommand()
        self.env = {
            'runtime': {
                'settingsManager': mock.MagicMock(),
                'memoryManager': mock.MagicMock(),
                'outputManager': mock.MagicMock(),
                'screenManager': mock.MagicMock(),
            }
        }
        self.env['runtime']['settingsManager'].getSettingAsInt.return_value = 10
        self.cmd.initialize(self.env)

    def test_paste_empty_clipboard(self):
        self.env['runtime']['memoryManager'].isIndexListEmpty.return_value = True

        self.cmd.run()

        self.env['runtime']['screenManager'].injectTextToScreen.assert_not_called()

    def test_paste_converts_newlines_to_carriage_returns(self):
        self.env['runtime']['memoryManager'].isIndexListEmpty.return_value = False
        self.env['runtime']['memoryManager'].getIndexListElement.return_value = "line 1\nline 2\nline 3"

        self.cmd.run()

        self.env['runtime']['screenManager'].injectTextToScreen.assert_called_once_with(
            "line 1\rline 2\rline 3"
        )

    def test_paste_crlf_conversion(self):
        self.env['runtime']['memoryManager'].isIndexListEmpty.return_value = False
        self.env['runtime']['memoryManager'].getIndexListElement.return_value = "line 1\r\nline 2\r\nline 3"

        self.cmd.run()

        self.env['runtime']['screenManager'].injectTextToScreen.assert_called_once_with(
            "line 1\rline 2\rline 3"
        )


class TestScreenDriverInjection(unittest.TestCase):
    def setUp(self):
        with mock.patch('os.system'):
            self.vcsa = VcsaDriver()
        self.vcsa_env = {
            'screen': {'newTTY': '1'},
            'runtime': {
                'attributeManager': mock.MagicMock(),
                'processManager': mock.MagicMock(),
                'debug': mock.MagicMock(),
            }
        }
        self.vcsa.initialize(self.vcsa_env)

    @mock.patch('fcntl.ioctl')
    @mock.patch('builtins.open', mock.mock_open())
    def test_vcsa_driver_injects_carriage_return_for_newlines(self, mock_ioctl):
        self.vcsa.injectTextToScreen("line1\nline2\r\nline3")

        injected_chars = [call[0][2] for call in mock_ioctl.call_args_list if call[0][1] == termios.TIOCSTI]
        injected_text = "".join(injected_chars)

        self.assertEqual(injected_text, "line1\rline2\rline3")
        self.assertNotIn("\n", injected_text)

    @mock.patch('fcntl.ioctl')
    @mock.patch('builtins.open', mock.mock_open())
    def test_vcsa_driver_injects_bytes_with_newlines(self, mock_ioctl):
        self.vcsa.injectTextToScreen(b"line1\nline2")

        injected_chars = [call[0][2] for call in mock_ioctl.call_args_list if call[0][1] == termios.TIOCSTI]
        injected_text = "".join(injected_chars)

        self.assertEqual(injected_text, "line1\rline2")

    @mock.patch('os.write')
    def test_pty_driver_injects_carriage_return_for_terminal_input(self, mock_write):
        driver = PtyDriver()
        mock_p_out = mock.MagicMock()
        mock_p_out.fileno.return_value = 42
        driver.p_out = mock_p_out

        driver.injectTextToScreen("echo hello\necho world\n")

        mock_write.assert_called_once_with(42, b"echo hello\recho world\r")

    @mock.patch('os.write')
    def test_pty_driver_injects_bytes_with_newlines(self, mock_write):
        driver = PtyDriver()
        mock_p_out = mock.MagicMock()
        mock_p_out.fileno.return_value = 42
        driver.p_out = mock_p_out

        driver.injectTextToScreen(b"echo hello\necho world\r\n")

        mock_write.assert_called_once_with(42, b"echo hello\recho world\r")

    @mock.patch('os.write')
    def test_pty_driver_preserves_newlines_for_stdout(self, mock_write):
        driver = PtyDriver()
        mock_p_out = mock.MagicMock()
        mock_p_out.fileno.return_value = 42
        driver.p_out = mock_p_out

        stdout_fd = sys.stdout.fileno()
        driver.injectTextToScreen(b"output from child\nsecond line\n", screen=stdout_fd)

        mock_write.assert_called_once_with(stdout_fd, b"output from child\nsecond line\n")


if __name__ == '__main__':
    unittest.main()
