import unittest
from io import StringIO
from unittest.mock import mock_open, patch
from file_filter import filter_file


class TestFileFilter(unittest.TestCase):
    def test_basic_functionality(self):
        content = "apple Banana\nOrange\n"
        with patch("builtins.open", mock_open(read_data=content)):
            result = list(filter_file("dummy.txt", ["apple"], []))
            self.assertEqual(result, ["apple Banana"])

    def test_stop_word_filtering(self):
        content = "apple stop\nBanana\n"
        result = list(filter_file(StringIO(content), ["apple"], ["stop"]))
        self.assertEqual(result, [])

    def test_case_insensitivity(self):
        content = "Apple BANANA\n"
        result = list(filter_file(StringIO(content), ["apple"], []))
        self.assertEqual(result, ["Apple BANANA"])
        result = list(filter_file(StringIO(content), ["apple"], ["banana"]))
        self.assertEqual(result, [])

    def test_file_object_input(self):
        content = StringIO("test line\nanother line\n")
        result = list(filter_file(content, ["test"], []))
        self.assertEqual(result, ["test line"])

    def test_multiple_matches(self):
        content = "apple apple banana\n"
        result = list(filter_file(StringIO(content), ["apple"], []))
        self.assertEqual(result, ["apple apple banana"])

    def test_empty_lines(self):
        content = "\n\napple\n"
        result = list(filter_file(StringIO(content), ["apple"], []))
        self.assertEqual(result, ["apple"])

    def test_edge_cases(self):
        # Both search and stop words in line
        content = "apple stop\n"
        result = list(filter_file(StringIO(content), ["apple"], ["stop"]))
        self.assertEqual(result, [])

        # Different case in search words
        content = "Apple\n"
        result = list(filter_file(StringIO(content), ["APPLE"], []))
        self.assertEqual(result, ["Apple"])

        # Empty search words
        result = list(filter_file(StringIO("test"), [], []))
        self.assertEqual(result, [])

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            list(filter_file("nonexistent.txt", ["test"], []))


if __name__ == "__main__":
    unittest.main()
