import argparse
import re

# Parses command line parameters and returns them
def parseArgs():
    parser = argparse.ArgumentParser(
        prog='cleantext',
        description='Prepares a text for rendering to MP3 by removing problematic text')
    parser.add_argument('file', help="The path to the text file to be cleaned")
    return parser.parse_args()

def main():  
    # Parse command line arguments
    args=parseArgs()

    if args.file != None:
        # Read the content of the file
        with open(args.file, 'r') as file:
            content = file.read()

        pattern_to_remove = r'<http.*?>'
        # Compile the pattern with re.DOTALL to handle multi-line patterns
        regex = re.compile(pattern_to_remove, re.DOTALL)

        # Remove the pattern from the content
        modified_content = regex.sub('', content)

        # Write the output file
        outfile=args.file + ".cleaned.txt"
        with open(outfile, 'w') as file:
            file.write(modified_content)

if __name__ == "__main__":
  main()