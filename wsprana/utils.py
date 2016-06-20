# -*- coding: utf-8 -*-
"""
General utilities module for WSPR-Ana

"""

import csv
import datetime

#--------------------------------------------------------- Get CSV Column Count
def csv_column_count(in_file):
    """
    Get the number of columns in a CSV files

    Parameters
    ----------
    in_file -- Path including file name

    For Example, running in the same direcory as 'data.csv':

    in_file = (os.getcwd() + (os.sep) + 'data.csv')

    Returns
    -------
    ccount -- number of columns in csv file (in_file)

    """
    try:
        with open(in_file, 'r') as csv_file:
            ccount = len(csv_file.readline().split(','))
            csv_file.close()
        return ccount
    except IOError as io_error:
        file_io_error_msg(io_error)
        exit()

#--------------------------------------------------------- Get CSV Record Count
def csv_record_count(in_file):
    """
    Get the number of records in a CSV files

    Parameters
    ----------
    in_file -- Path including file name

    For Example, running in the same direcory as 'data.csv':

    in_file = (os.getcwd() + (os.sep) + 'data.csv')

    Returns
    -------
    rcount --number of records in csv file (in_file)

    """
    try:
        with open(in_file, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=",")
            data = list(reader)
            rcount = len(data)
            csv_file.close()
        return rcount
    except IOError as io_error:
        file_io_error_msg(io_error)
        exit()

#----------------------------------------------------------- Raw Input Callsign
def enter_callsign():
    r"""
    Command line callsign entry

    Parameters
    ----------
    user-input -- Prompts the user for single or multiple call signs
        separated buy commas ',', for example: KI7MT,K1ABC,K1DEF,K1GHI

    Returns
    -------
    call in upper case

    """
    call = input("Enter callsign: ")
    call = call.upper()
    return call

#----------------------------------------------------------- Convert Epoch Date
def convert_epoch_date(ecpch_time_stamp)
    """Converts unix epoch time in seconds to date
    
    Parameters
    ----------
    Epoch time in seconds
    
    Returns
    -------
    utc_date: %Y-%m-%d

    """
    timestamp = (ecpch_time_stamp)
    initial_value = datetime.datetime.fromtimestamp(ecpch_time_stamp)
    utc_date = (value.strftime('%Y-%m-%d'))
    return utc_date

#----------------------------------------------------------- Convert Epoch Time
def convert_epoch_time(ecpch_time_stamp)
    r"""Convert epoch time in seconds to time
    
    Parameters
    ----------
    Epoch time in seconds
    
    Returns
    -------
    utc_date: %H%M

    """
    timestamp = (ecpch_time_stamp)
    initial_value = datetime.datetime.fromtimestamp(ecpch_time_stamp)
    utc_time = (value.strftime('%H%M'))
    return utc_time


###############################################################################
# GENERAL ERROR MESSAGES
###############################################################################

#--------------------------------------------------------- File IOError Message
def file_io_error_msg(io_error):
    """File missing or bad path IOError Message"""
    print("")
    print(io_error)
    print("Check file exists, path is correct, and file is not currupt.")
    print("")

