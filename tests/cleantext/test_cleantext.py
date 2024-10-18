import unittest
import subprocess
import os

testDir=os.path.dirname(__file__) + '/'
cleantextpath=testDir + '../../python/cleantext.py'
#cleantextpath='python/cleantext.py'
stdoutfile='/tmp/test_cleantext_stdout.txt'
tempdir='/tmp/'
cleanedFilePath=tempdir + 'testCleantext_cleaned.txt'

testResourcesDir='./'
testInputsDir=testDir + 'inputs/'
testExpectedResultsDir=testDir + 'expected_results/'

def runCleanText(source, output_reference, cleantextArgs=None):
    """
    This function runs cleantext, saving the cleaned file and redirecting stdout and strderr to the temp dir

    Parameters:
    source - The source file that will be cleaned
    output_reference - The output reference file.  The file produced by cleantext will be compared to this.
    args - Any arguments that will be passed to cleantext when it is run.
    """
    
    # Build up arguments list for exec call
    execArgs=[cleantextpath]
    if cleantextArgs != None:
        execArgs += cleantextArgs
    execArgs+=[testInputsDir + source, cleanedFilePath]

    # Run cleantext
    subprocess.run(execArgs)

    # Check the output

class TestCleantext(unittest.TestCase):
    # Test that markup patterns are removed from a file
    def test_remove_markup(self):
        runCleanText('removeMarkup.txt', 'removeMarkup.txt')

if __name__ == '__main__':
    unittest.main()