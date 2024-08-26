#!/bin/bash

MODE=$1 # Either "dirs" or "files", depending on the type of input
shift
SCRIPT=$1
shift
TYPE=""
if [ $1 = "-t" ]
then
    TYPE=$2 # Used if softenv analysis
    shift
    OUTPUT=$2
    shift
else
    OUTPUT=$1
fi
shift
INPUT="$@"

# Adding option prefix:
if [ "$TYPE" != "" ]
then
    TYPE="-t $TYPE"
fi

# If inputs are files, then we just use that as input for the script:
INPUT_FILES=$INPUT
# If inputs are directories, we need to explore every single one of them
# to find the input files to pass to the script:
if [ $MODE = "dirs" ]
then
    INPUT_FILES=""
    for dir in $INPUT
    do
        INPUT_FILES="$INPUT_FILES $(find $dir/*.csv -maxdepth 1 -type f)"
    done
fi

python3 $SCRIPT $TYPE -i $INPUT_FILES -o $OUTPUT