#!/usr/bin/env bash
#
# Note: This script uses parallel Giz (pigz)
#       to decompress the gz files. If you do
#       not have it installed, perform the following
#
#  sudo add-apt-repository universe
#  sudo apt-get install pigz
# 
# Usage:
#
#   Execute the command: ./convert.sh
#
set -e 

#################################################
## USER EDITABLE VARIABLES
#################################################

# Year of the wpsrspots file
declare -a year=(2008)

# month of the wsprspots file
declare -a month=(03)

#################################################
## --   no edits needed below this line   --  ##
#################################################

DEBUG=1

clear ||:

# Scala Application name
APP_NAME="ConvertCsvToParquet-assembly-1.0.jar"

# number of CPU cores to use
CORES=$(nproc)

# WA_CSVROOT = is the root of your WSPRnet CSV repository
# Check if WA_CSVROOT Directory is set
if [ -z ${WA_CSVROOT+x} ]; then
    echo "Environment Variable Error: WA_CSVROOT is unset";
    echo 'Check the documentation for setting this environment variable'
    echo ''
    exit 1
else
    if [ "$DEBUG" = 1 ]; then
        echo "CSV Root Directory is set to ......: $WA_CSVROOT";
    else
        :
    fi
fi

# WA_PQROOT = is the root  of your Parquet Repository
# Check if WA_PQROOT Directory is set
if [ -z ${WA_PQROOT+x} ]; then
    echo "Environment Variable Error: WA_PQROOT is unset";
    echo 'Check the documentation for setting this environment variable'
    echo ''
    exit 1
else
    if [ "$DEBUG" = 1 ]; then
        echo "Parquet Root Dicrectory is set to .: $WA_PQROOT";
        echo ''
    else
        :
    fi
fi

# Make PUSHD be quiet
pushd () {
    command pushd "$@" > /dev/null
}

# make POPD be quiet
popd () {
    command popd "$@" > /dev/null
}

# outer loop for years
echo 'Processing Requested Files (this takes a while...)'
for y in "${year[@]}"
do
    # inner loop for months
    for m in "${month[@]}"
    do
        infile="$WA_CSVROOT/wsprspots-$y-$m.csv"
        outdir="$WA_PQROOT/$y/$m"
        gzfile="$WA_CSVROOT/wsprspots-$y-$m.csv.gz"

        # Remove old decompressed file
        rm -f "$infile" > /dev/null 2>&1

        # -d decompress, -k keep the original file, -f force overwrite
        echo "Decompress    : $gzfile"
        
        # decompress the csv.gz file
        pigz -dkf "$WA_CSVROOT/wsprspots-$y-$m.csv.gz"

        #echo "In File ......: $infile"
        #echo "Archive File .: $gzfile"
        #echo "Out Dir ......: $outdir"

        # move into the Java jars folder
        pushd ../jars

        # run the convert command
        `which spark-submit` --master=local["$CORES"] "$APP_NAME" "$infile" "$outdir"

        # pop back out to original location
        popd

        # check for success markers
        ls -alh $outdir | grep "_SUCCESS.crc"
        echo ""
    done
done

exit 0