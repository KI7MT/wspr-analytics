import os
import time
import argparse

from os import system, name
from os.path import getsize

import pandas as pd

# if you get a seg-fualt on LZ4 or BROTLI, incewase the sleep a by .5 or 1.0
sleep_time = 2.5

parquet_types = ['SNAPPY', 'LZ4', 'ZSTD', 'GZIP', 'BROTLI']

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


# define our clear function 
def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

def get_file_size(csvfile, comp_type):
    """Get the size of a fiz in MB"""
    file_path = csvfile.replace('csv', comp_type.lower())
    
    return getsize(file_path) / 1048576


# Use Pandas to read CSV files
def pandas_convert_csv(csvfile):
    """
    Convert the CSV file using parquet_type compression
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
