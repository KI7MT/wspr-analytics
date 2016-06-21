# -*- coding: utf-8 -*-
"""
General utilities for WSPR Analysis

"""

import os
import sys
import csv
import datetime
from time import gmtime

#--------------------------------------------------------- Get CSV Column Count
# TO-DO: this function is not implmented yet
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
# TO-DO: this function is not implmented yet
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
# TO-DO: this function is not implmented yet
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
# TO-DO: this function is not implmented yet
def convert_epoch_date(epoch_time_stamp):
    """Converts unix epoch time in seconds to date

    Parameters
    ----------
    Epoch time in seconds

    Returns
    -------
    utc_date: %Y-%m-%d

    """
    initial_value = datetime.datetime.fromtimestamp(epoch_time_stamp)
    utc_date = (initial_value.strftime('%Y-%m-%d'))
    return utc_date

#----------------------------------------------------------- Convert Epoch Time
# TO-DO: this function is not implmented yet
def convert_epoch_time(epoch_time_stamp):
    r"""Convert epoch time in seconds to time

    Parameters
    ----------
    Epoch time in seconds

    Returns
    -------
    utc_date: %H%M

    """
    initial_value = datetime.datetime.fromtimestamp(epoch_time_stamp)
    utc_time = (initial_value.strftime('%H%M'))
    return utc_time

#--------------------------------------------------- Convert Epoch lines in CSV
# TO-DO: this function is not implmented yet
def convert_epoch_lines():
    r"""Convert lines in CSV file from epoch to human readable

    Parameters
    ----------
    in_file is the source CSV file, path and file name
    out_file is the output, path and file name

    Returns
    -------
    New CSV file with epoch dattime stamp coverted to date,time

    Important: the file must be in the form of WSPRnet CSV archive files, e.g.
     field [1] must be the epoch time stamp.

    """
    now = DATE_TIME.strftime("%Y-%m")
    appdir = os.getcwd()
    REPORTS_PATH = ''
    os.chdir(REPORTS_PATH)
    csv_file = ''
    mylogfile = REPORTS_PATH + (os.sep) + now + '-' + call + '-converted.csv'
    try:
        w = open(mylogfile, "w")
        r = open(csv_file, 'r')
        for line in r:
            x = line.split(',')
            epoch_time_stamp = float(x[1])                      # get epoch date/time
            utc_date = convert_epoch_date(epoch_time_stamp)     # get time
            utc_time = convert_epoch_time(epoch_time_stamp)     # get date
            timestamp = str(utc_date) + ',' + str(t)            # combine date , time
            newl = x[0] + ',' + timestamp                       # create new line beginning
            for count in range (len(x)-2):                      # re-combine the line
                newl = newl + ',' + x[count+2]
            w.write(newl,)                                      # write the new line to file
        r.close()                                               # close in_file
        w.close()                                               # close out_file
        os.chdir(appdir)                                        # go back to script directory
    except IOError as io_error:
        file_io_error_msg(io_error)
        os.chdir(appdir)
        exit()

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

