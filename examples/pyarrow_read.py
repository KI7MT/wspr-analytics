import os
import time
import argparse

from os import system, name
from os.path import getsize

import pyarrow.csv as pv
import pyarrow.parquet as pq


read_types = ['CSV', 'SNAPPY', 'ZSTD', 'GZIP', 'BROTLI']


def clear():
    """
    Clear screen function for Windows Linux and MacOS
    """
    if name == 'nt': 
        _ = system('cls') 
    else: 
        _ = system('clear') 


def get_file_size(csvfile, comp_type):
    """
    Get the size of a fiz in MB
    """
    file_path = csvfile.replace('csv', comp_type.lower())
    
    return getsize(file_path) / 1048576


def pyarrow_read(csvfile):
    """
    Read the files with varying reads
    """
    print("Running Read Tests Using Apache Arrow")
    print(f"Compression Types : {read_types}\n")
    for f in read_types:
        ext = str(f.lower())
        
        if f.lower() == 'csv':
            file_name = csvfile
            short_name = os.path.basename(csvfile)
            print(f'* Reading file  : {short_name}')
        else:
            file_name = csvfile.replace('csv', ext.lower())
            short_name = os.path.basename(file_name)
            print(f'* Reading file  : {short_name}')
        
        # PyArrow uses a different read method for CSV files (read_csv v.s. read_table)
        start = time.time()
        if f.lower() == 'csv':
            reader = pv.read_csv(file_name)
        else:
            pfile = pq.read_table(file_name)
        end = time.time()

        print(f"* File Size     : {round(get_file_size(csvfile, ext), 2)} MB")
        print(f"* Elapsed Time  : {round((end - start), 3)}\n")


if __name__ == '__main__':
    clear()
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', dest='filename', type=str, required=True,
                        help='Path to CSV file to process')

    args = parser.parse_args()

    if args.filename:
        pyarrow_read(args.filename)
    
    print("\n Finished !!\n")