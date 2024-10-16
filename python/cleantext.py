#!/mnt/linuxdata/james/code/venv_python/bin/python

import argparse
import re

# Parses command line parameters and returns them
def parseArgs():
    parser = argparse.ArgumentParser(
        prog='cleantext',
        description='Prepares a text for rendering to MP3 by removing problematic text')
    parser.add_argument('file', help="The path to the text file to be cleaned")
    parser.add_argument('output', help="The file that the cleaned text will be output to", nargs='?', default=None)
    parser.add_argument('--urls', help="Remove URLs", default=True)
    parser.add_argument('--markup', help="Remove characters commonly left in text from web pages (such as * and /)", default=True)
    return parser.parse_args()

def removeRegex (text, pattern_to_remove, multiline=False):
    if multiline==True:
        # Compile the pattern with re.DOTALL to handle multi-line patterns
        regex = re.compile(pattern_to_remove, re.DOTALL)
    else:
        regex = re.compile(pattern_to_remove)
    
    return regex.sub('', text)


# Remove '*' and '/'
def removeMarkup(text):
    # Remove forward slashes at the start of a line
    removeRegex(text, r'$/')

# For future use (not currently used) removing duplicate lines from files, useful when removing a header/footer
def getDuplicates(args):
  print('Scanning file ' + args.filename)

  lineFoundCount = defaultdict(int) # The key will be the string that was found, the value will be the number of times it was found
  duplicatelines=[]

  # Go through the file looking for duplicate lines
  with open(args.filename) as inputfile:
      for linenum, rawline in enumerate(inputfile):
          thisline = rawline.strip()
          if thisline:
              # Increment the count for this line, or add it if it isn't already there
              lineFoundCount[thisline] += 1

              # Add to our list of duplicate lines if it isn't already there
              if lineFoundCount[thisline] > 1 and thisline not in duplicatelines:
                duplicatelines.append(thisline)

      # Print any duplicate lines that were found along with the number of times they were found
      print("Duplicate lines found:")
      for thisline in duplicatelines:
        print("{:<100}{}".format(thisline, lineFoundCount[thisline]))

def logmsg(message):
    print(message)

def main():  
    # Parse command line arguments
    args=parseArgs()

    if args.file != None:
        # Read the content of the file
        with open(args.file, 'r') as file:
            content = file.read()

        if args.urls:
            # Remove URLs
            modified_content = removeRegex(content, r'<http.*?>', multiline=True)
        
        if args.markup:
            # Remove '*' and '/'
            removeMarkup(content)

        # Write the output file
        if args.output==None:
            outfile=args.file + ".cleaned.txt"
        else:
            outfile=args.output
        logmsg( "Writing cleaned text to " + outfile)


        with open(outfile, 'w') as file:
            file.write(modified_content)

if __name__ == "__main__":
  main()