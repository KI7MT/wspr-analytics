#/usr/bin/env bash

# Description: Small shell wrapper for downloading WSPRnet CSV Files

# Save this script as: ..: test-csvdl.sh
# Update Permissions ....: chmod +x ./test-csvdl.sh
# Run the script with  ..: ./test-csvdl.sh

set -e

# Destination path
DOWNLOAD_DIR="/data/raw/csv"

# this will download the months 03,04, and 05 for 2008
declare -a year=(2021)
declare -a month=(01 02)

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
ls -alh "$DOWNLOAD_DIR"
echo ''

# exit the script
exit 0

# NOTE:
#   You could also add getopts to allow for command line input for the year / month
#   combnations if desired.
