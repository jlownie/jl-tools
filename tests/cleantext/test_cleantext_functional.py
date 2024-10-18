# This script contains functional tests for cleantext

import unittest
from tests.cleantext.testing_framework import runCleanText

class TestCleantext(unittest.TestCase):
    # Test that markup patterns are removed from a file
    def test_remove_markup(self):
        runCleanText('removeMarkup.txt', 'removeMarkup.txt')

if __name__ == '__main__':
    unittest.main()