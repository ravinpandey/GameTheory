#!/bin/bash

# Example script for the Othello assignment. Make sure to make it executable (chmod +x othello)
# Change the last line (python3 Othello.py ...) if necessary
#
# usage: bash othello <position> <time_limit>

position=$1
time_limit=$2

# Run the Python program with the given position and time limit
python3 Othello.py $position $time_limit
