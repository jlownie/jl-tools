# This script contains unit tests for cleantext

# Standard libs
import unittest

# Testing libs
import tests.cleantext.testing_framework as framework
from tests.cleantext.testing_framework import getMainArgs

# Project libs
import python.cleantext as cleantext

class TestCleantextUnit(unittest.TestCase):
    # Test that markup patterns are removed from a file
    # This duplicates the functional test case of the same name and was created to assist with debugging
    def test_remove_markup(self):
        args=getMainArgs('removeMarkup.txt')
        cleantext.main(args)

    def test_output_unspecified(self):
        args=getMainArgs('removeMarkup.txt')
        args.output=None
        cleantext.main(args)

if __name__ == '__main__':
    unittest.main()