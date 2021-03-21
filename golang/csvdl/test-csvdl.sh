#/usr/bin/env bash

# Description: Small shell wrapper for downloading WSPRnet CSV Files

# Save this script as: ..: test-csvdl.sh
# Update Permissions ....: chmod +c ./test-csvdl.sh
# Run the script with  ..: ./test-csvdl.sh

set -e

# Destination path
DOWNLOAD_DIR="$HOME/Downloads/wsprnet"

# this will download the months 03,04, and 05 for 2008
declare -a year=(2008)
declare -a month=(03 04 05)

# clear the screen
clear ||:

# outer loop for years
for y in "${year[@]}"
do
    # inner loop for months
    for m in "${month[@]}"
    do
        # download invocation
        ./csvdl --year="$y" --month="$m" --dest="$DOWNLOAD_DIR"
    done
done

# list items in the custom output location
ls -al "$DOWNLOAD_DIR"
echo ''

# exit the script
exit 0

# NOTE:
#   You could also add getopts to allow for command line put for the year month
#   combnations if desired.