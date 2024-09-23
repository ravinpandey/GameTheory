#!/bin/bash

# Arguments: 
# $1: ASCII string of length 65 representing the game position
# $2: Time limit in seconds
# $3: Compilation flag (1 for compile, 0 for run)

# Validate input
if [ "$#" -ne 3 ]; then
    echo "Error: Incorrect number of arguments."
    echo "Usage: ./othello.sh <position> <time_limit> <do_compile>"
    exit 1
fi

# Validate position string length
if [ "${#1}" -ne 65 ]; then
    echo "Error: Position string must be 65 characters long."
    exit 1
fi

# Validate first character (W or B)
if [[ "$1" != W* && "$1" != B* ]]; then
    echo "Error: First character must be 'W' or 'B'."
    exit 1
fi

# Validate remaining characters (E, O, X)
if ! [[ "${1:1}" =~ ^[EOX]{64}$ ]]; then
    echo "Error: Board description must contain only 'E', 'O', or 'X' for empty, white, or black markers."
    exit 1
fi

# Capture inputs
position="$1"
time_limit="$2"
do_compile="$3"

# Check if Python or Java should be executed
if [ "$do_compile" -eq 1 ]; then
    # Compile Java if needed
    if [ -f "Othello.java" ]; then
        javac Othello.java
        if [ $? -ne 0 ]; then
            echo "Error: Compilation failed."
            exit 1
        fi
        echo "Compilation successful."
    else
        echo "Python does not need compilation."
    fi
elif [ "$do_compile" -eq 0 ]; then
    # Run Python or Java
    if [ -f "../Python/Othello.py" ]; then
		#echo "Behanchod Run Nhi Ho Raha Hai"
        python3 -u ../Python/Othello.py "$position" "$time_limit"
    elif [ -f "Othello.class" ]; then
        java Othello "$position" "$time_limit"
    else
        echo "Error: No executable found (Othello.py or Othello.class)."
        exit 1
    fi
else
    echo "Error: Invalid compilation flag (must be 0 or 1)."
    exit 1
fi
