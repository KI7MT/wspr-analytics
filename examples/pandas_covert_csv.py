"""
    Filename: pandas_convert_csv.py

    This script takes in one command-line argument -f <filename> and
    converts the CSV in to an Apache Parquet compressed format (x5)

    Formats: 'SNAPPY', 'LZ4', 'ZSTD', 'GZIP', 'BROTLI'

    The default format for Parguet is "SNAPPY". The end result is
    five new files:

        wsprspots-yyyy-mm.['snappy', 'lz4', 'zstd', 'gzip', 'brotli']

    The script uses Pandas, which is not the fastest library we could
    use to do the convertion. It's here as a reference to compare
    other methods of converstion.

    This script applies the data_type listed beliow, as well as
    column headers for reference. There is "No" data transformation,
    though it is needed.

    Transformation (for analytics only)

        Areas where the original CSV could be improved (new file schema):
        - timestame: break out into <2020-MM-DD>
        - timestame: break the time into 0000 UTC
        - band: should be converted to common language (20m, 10m, 80m, etc)
        - power: convert dbm to actual power level 1w, 1mw, etc
        - version: fill in nulls with some value. Early years did not rport this column

    Partitioning (for analytics only):

        There are a number of partitioning schemas that could serve the data set well.
        Getting general agreement on how it should be broken out would be a challange
        due to the vast number of use cases.
"""
import os
import time
import argparse

from os import system, name
from os.path import getsize

import pandas as pd

# if you get a seg-fualt on LZ4 or BROTLI, increase the sleep a by .5 or 1.0
sleep_time = 2.5

# These are the common Parquet compression types. Parquet's default in 'snappy'.
parquet_types = ['SNAPPY', 'LZ4', 'ZSTD', 'GZIP', 'BROTLI']


# Defind the stat structures for the original CSV file
spot_dtype = {'Spot_ID': 'string',
              'TimeStamp': 'int',
              'Reporter': 'string',
              'RxGrid': 'string',
              'SNR': 'int',
              'Frequency': 'double',
              'CallSign': 'string',
              'Grid': 'string',
              'Power': 'int',
              'Drift': 'int',
              'Distance': 'int',
              'Azimuth': 'int',
              'Band': 'int',
              'Version': "string",
              'Code': 'int'
              }


# Column names for the dataframe
column_names = ['Spot_ID',
                'TimeStamp',
                'Reporter',
                'RxGrid',
                'SNR',
                'Frequency',
                'CallSign',
                'Grid',
                'Power',
                'Drift',
                'Distance',
                'Azimuth',
                'Band',
                'Version',
                'Code'
                ]
def clear():
    """
    Clear screen function for Windows Linux and MacOS
    """
    if name == 'nt': 
        _ = system('cls') 
    else: 
        _ = system('clear')


def get_file_size(csvfile, comp_type):
    """Get the size of a fiz in MB"""
    file_path = csvfile.replace('csv', comp_type.lower())
    
    return getsize(file_path) / 1048576


def pandas_convert_csv(csvfile):
    """
    Convert CSV file using parquet_type compression
    """
    file_name = os.path.basename(csvfile)

    clear()
    print("\nPandas CSV Conversion Method")
    print(f"Parquet Compression Types : {parquet_types}")
    print("Sit back and relax, this takes a while!!\n")
    print(f'* Reading file  : {file_name}')
 
    start = time.time()
    df = pd.read_csv(csvfile, dtype=spot_dtype, names=column_names, header=None)
    rc = df.shape[0]
    print(f"* Spot Count    : {rc:,}")
    end = time.time()
    print(f"* File Size     : {round(get_file_size(csvfile, 'csv'), 2)} MB")
    print(f"* Elapsed Time  : {round((end - start), 3)} sec")

    for f in parquet_types:
        compression_type = str(f.upper())
        file_name = csvfile.replace('csv', f.lower())
        if compression_type == "PARQUET":
            comp_type = "NONE"
        else:
            comp_type = compression_type.upper()
        print(f'\n* Converting CSV to -> {f.lower()}')
        start = time.time()
        df.to_parquet(file_name, compression=str(comp_type.upper()))
        end = time.time()
        time.sleep(sleep_time) # prevent seg-fault on reads that are too quick

        print(f"* File Size     : {round(get_file_size(csvfile, comp_type), 2)} MB")
        print(f"* Elapsed Time  : {round((end - start), 3)} sec")


if __name__ == '__main__':
    clear()
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', dest='filename', type=str, required=True,
                        help='Path to CSV file to process')

    args = parser.parse_args()

    if args.filename:
        pandas_convert_csv(args.filename)
    
    print("\nNOTE : The File Sizes Are Approximated = (file bytes / 1048576)")
    print("\n Finished !!\n")
