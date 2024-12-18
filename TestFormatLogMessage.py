# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 10:39:04 2024

@author: Shane
"""

import unittest
from learniverse_2024_12_18_09_17 import format_log_message  # Update import to match your file structure

class TestFormatLogMessage(unittest.TestCase):
    def test_format_log_message(self):
        """Test normal case for formatting log messages."""
        timestamp = "2024-12-18 10:00:00"
        message = "This is a log message."
        expected = "[2024-12-18 10:00:00] This is a log message."
        self.assertEqual(format_log_message(timestamp, message), expected)

    def test_empty_message(self):
        """Test with an empty log message."""
        timestamp = "2024-12-18 10:00:00"
        message = ""
        expected = "[2024-12-18 10:00:00] "
        self.assertEqual(format_log_message(timestamp, message), expected)

    def test_empty_timestamp(self):
        """Test with an empty timestamp."""
        timestamp = ""
        message = "Log with no timestamp."
        expected = "[] Log with no timestamp."
        self.assertEqual(format_log_message(timestamp, message), expected)

    def test_empty_both(self):
        """Test with both timestamp and message empty."""
        timestamp = ""
        message = ""
        expected = "[] "
        self.assertEqual(format_log_message(timestamp, message), expected)

# Run the test
if __name__ == "__main__":
    unittest.main()
