# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 09:25:45 2024

@author: Shane
"""

import unittest
from datetime import datetime
# from your_module import get_current_timestamp  # Replace 'your_module' with your filename
# from ..learniverse_2024_12_18_09_17 import get_current_timestamp
from learniverse_2024_12_18_09_17 import get_current_timestamp



class TestGetCurrentTimestamp(unittest.TestCase):
    def test_format(self):
        """
        Test if the function returns a timestamp in the correct format.
        """
        timestamp = get_current_timestamp()

        # Check if it's a string
        self.assertIsInstance(timestamp, str)

        # Check if it matches the expected format
        try:
            datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            self.fail("Timestamp is not in the correct format 'YYYY-MM-DD HH:MM:SS'")

# Run the test
if __name__ == "__main__":
    unittest.main()
