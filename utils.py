# -*- coding: utf-8 -*-
"""
General utilities module for WSPR-Ana

"""

import csv

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
    ccount --- Returned number of columns in csv file

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
    rcount --- Returned number of columns in csv file

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
    call -- in upper case

    """
    call = input("Enter callsign: ")
    call = call.upper()
    return call

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





