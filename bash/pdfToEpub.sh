logFileName=pdfToEpubLog.txt
logFileInitialised="false"

function initialiseLogFile ()
{
	date > "$destPath$logFileName"
	logFileInitialised="true"
	return
}

function logMsg()
{
	# Check that a parameter has been passed in
	if [ -z "$1" ]; then
		return
	fi

	# Initialise the log if necessary
	if [ "$logFileInitialised" == "false" ]; then
		initialiseLogFile
	fi
	echo "$1" >> "$destPath$logFileName"
	return

	echo $1 >> $logFileName
	echo $1
}

#####################################
### Program execution starts here ###
#####################################

# Validate input
if [ -z "$1" ]; then
	printusage
	exit
fi

# Clear the log
rm $logFileName

# Check if running from Nautilus or command line
if [ -n "$NAUTILUS_SCRIPT_SELECTED_FILE_PATHS" ]; then
	inputPaths=$NAUTILUS_SCRIPT_SELECTED_FILE_PATHS
else
	inputPaths="$@"
fi

# Start the log
destPath=$(echo "$1" | grep -o '.*/')
logMsg "Running in $destPath"

# Take out spaces in the file names (they will be put back in later)
inputPaths=$(echo "$inputPaths" | tr " " "\246")
logMsg "Input file(s) $inputPaths"

for sourcefile in $inputPaths; do
	# Put the newlines back into the file name
	sourcefile=$(echo $sourcefile | tr "\246" " ")
	# Thunar sometimes puts quotes in which need to be stripped out
	sourcefile=$(echo $sourcefile | tr -d \')

	# Read the file into memory
	logMsg "Processing file $sourcefile"

	# determine the output file name
	destFile=$(echo $sourcefile | sed s/\\.pdf/.epub/)
	logMsg "input file is $sourcefile"
	logMsg "Destination file name is $destFile"
	#exit
	
	# do the conversion
	ebook-convert "$sourcefile" "$destFile" &>>$logFileName
	logMsg "Finished file"
done

logMsg "Script finished"
