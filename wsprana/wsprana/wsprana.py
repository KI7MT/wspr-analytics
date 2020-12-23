#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

r"""Module provides various functions in processing WSPRnet data files

    Application Directories
    -----------------------
    WSPR-Ana uses FSH or file system hierarchy. The following locations
    apply for both Windows and Linux:

    Linux: /home/<user-name>/.local/share/WSPR-ANA/{csvd,srcd,reports}

    Windows: C:\Users\<user-name>\AppData\Roaming\WSPR-ANA\{csvd,srcd,reports}
    
    If you have previously downloaded the WSPRnet archive files, ensure you
    move any *.gz / *.zip file to the 'srcd" directory.

    Likewise, if you have extracted CSV files, ensure they are copied or moved
    to the 'csvd' directory.

"""

import csv
import datetime
import glob
import gzip
import hashlib
import mmap
import os
import sqlite3
import subprocess
import sys
import time
from time import gmtime
from builtins import input

import requests
from bs4 import BeautifulSoup
from clint.textui import progress
from appdirs import AppDirs
import utils as ut

#--------------------------------------------------- global variables and paths

# set FSH path locations using AppDirs
dirs = APP_DIR = AppDirs("WSPR-ANA", appauthor='', version='', multipath='')
APP_DIR = dirs.user_data_dir
BASE_PATH = (os.getcwd())

# set db and sql names
DB_NAME = 'wsprana.db'
SQL_FILE = (BASE_PATH + (os.sep) + 'wsprana.sql')

# set path vvariables
CSV_PATH = (APP_DIR + (os.sep) + "csvd")
DB_PATH = (APP_DIR + (os.sep) + DB_NAME)
REPORTS_PATH = (APP_DIR + (os.sep) + "reports")
SRC_PATH = (APP_DIR + (os.sep) + 'srcd')
R_SCRIPT_PATH = (os.getcwd() + (os.sep) + "rscripts")

# general variables
DIR_LIST = [APP_DIR, SRC_PATH, CSV_PATH, REPORTS_PATH]
DATE_TIME = datetime.date.today()
DWN_LIST = []
BASE_URL = "http://wsprnet.org/archive/"
OS_EXT = ''

#------------------------------------------------------ Help and Docstring Data


def a_help():
    """WSPRANA Help and General Information

    REQUIREMENTS:

    Python2.5+ or Python3.0+ interrupter in your $PATH / %PATH%


    PYTHON MODULES:

    The following assumes a base install with no additional modules added. For
    Linux, you may also satisfy the requirements with your package manager
    if they are available.

        pip install beautifulsoup4
        pip install clint
        pip install requests

    For Debian / Ubuntu based distributions, you can install the required
    packages with:

        Python2
        sudo apt-get install python-bs4 python-clint python-requests

        Python3
        sudo apt-get install python3-bs4 python3-clint python3-requests


    INSTALLATION and USAGE:

    If you have already downloaded all the archive files from WSPRnet.org,
    copy them to the SRC_PATH directory after cloning.

        1. git clone git://git.code.sf.net/u/ki7mt/wspr-ana
        2. Copy previously downloaded WSPRNet archive files to ./wspr-ana/SRC_PATH
        3. To run, type: ./wsprana.py
        4. For the first run, select Option-1 to sync archive files
        5. Aer initial database sync, you can search all or the current
           month for a given callsign.


     OVERVIEW:

     Wspr-Ana provides a set of commonly used functions to download and parse
     database archive files from http://wsprnet.org.

     The download lists are generated directly from WSPRnet.org archive URL. As
     new files are added, they should be automatically picked up by and added
     to the process list. This includes the the current month which is updated
     in early hours UTC each day.

     The script should work with either Python2 or Python3. It will also auto
     select the extension based on running Windows (.zip) or Linux (.gz)


    STRUCTURE, VARIABLES and SCRIPTS:

    For the users convenience, a preloaded database has already been provided.
    This help prevent anomalies with downloads an initial status table updates.

    The folder and file structures are as follows:

        SRC_PATH ........: Directory for WSPRNet archive files
        CSV_PATH ........: Directory for extracted csv files
        REPORTS_PATH .....: Directory for output files
        wsprana .....: SQLite3 Database
        SQL_FILE ........: SQL template for pre-loading the database
        wsprana.py ..: Main script


     DEFAULT DATABASE:

     A default database, updated as of the latest git posting, is provided in
     the repository. The data contained in the [ status ] table contains the
     following fields:

     name ......: archive file name from WSPRNet
     date ......: the date the status was last updated
     column ....: the number of columns for the archive file
     records ...: the number of records in the archive .csv file"""

#----------------------------------------------------------- Set file extension
def set_ext():
    """Set Archive File Extension

    Actions Performed:
        1. For Windows, the extension is set to (zip)
        2. For Linux, the extension is set to (gz)"""
    global OS_EXT
    if sys.platform == "win32":
        OS_EXT = "zip"
    else:
        OS_EXT = "gz"

    return OS_EXT

#----------------------------------------------------------- Create directories
def create_dirs():
    """Create Script Directories

    Actions Performed:
        1. Creates directories if they do no exist"""
    for d in DIR_LIST:
        if not os.path.exists(d):
            os.makedirs(d)


#----------------------------------------------------------------- Reset timers
def reset_timers():
    """Reset Timer Values

    Actions Performed:
        1. Resets timers used in various functions"""
    qt1 = 0 # pylint: disable=unused-variable
    qt2 = 0 # pylint: disable=unused-variable
    qt3 = 0 # pylint: disable=unused-variable
    qt4 = 0 # pylint: disable=unused-variable
    qt5 = 0 # pylint: disable=unused-variable
    qt6 = 0 # pylint: disable=unused-variable
    qt7 = 0 # pylint: disable=unused-variable
    qt8 = 0 # pylint: disable=unused-variable
    qt9 = 0 # pylint: disable=unused-variable
    qt10 = 0 # pylint: disable=unused-variable


#----------------------------------------------------------------- Clean Screen
def clear_screen():
    """Clear Screen Based On Platform Type

    Actions Performed:
        1. Is Platform is Windows, use 'cls'
        2. Is Platform is Windows, use 'clear'"""
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')


#--------------------------------------------------------------- Pause function
def pause():
    """Pause Statement

    Actions Performed:
        1. Prompt the user for input to create a pause"""
    input("\nPress [ ENTER ] to continue...")

#--------------------------------------------------- Under Development Message
def under_development():
    print("\n" + 45 * '-')
    print(" Under Development")
    print(45 * '-')
    print("\n This feature is currently under development.")
    print("")


#---------------------------------------------------------- Initialize Database
def init_db():
    """Create Main Database

    Actions Performed:
        1. Open SQLit3 Database connection
        2. Execute SQL query to create tables
        3. Add script information to appdata table
        3. Print creation summary"""
    qt1 = time.time()
    print(50 * '-')
    print("Creating New WSPR Analysis Database")
    print(50 * '-')

    # connect to SQLite3 database
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        fd = open(SQL_FILE, 'r')
        script = fd.read()
        cur.executescript(script)
        fd.close()

        cur.execute('SELECT SQLITE_VERSION()')
        sv = cur.fetchone()

        cur.execute('SELECT * FROM appdata ORDER BY ROWID ASC LIMIT 1')
        for row in cur.fetchall():
            aut = row[0]
            cop = row[1]
            lic = row[2]
            ver = row[3]
            cnt = row[4]
            sta = row[5]

    conn.close()

    qt2 = (time.time() - qt1)
    print(" SQLite Version ....: %s" % sv)
    print(" Database Name .....: %s" % DB_NAME)
    print(" Database Version ..: %s" % ver)
    print(" Author ............: %s" % aut)
    print(" Contact ...........: %s" % cnt)
    print(" Copyright .........: %s" % cop)
    print(" License ...........: %s" % lic)
    print(" Status ............: %s" % sta)
    print(" Execution time ....: %.3f seconds" % qt2)
    print("\n")
    conn.close()
    time.sleep(2)


#------------------------------------------------------------ Get database info
def check_db():
    """Check Database Connection

    Actions Performed:
        1. Connect to database via the DB_PATH() function
        2. If the database does not exist, create it with init_db()"""
    if os.path.isfile(DB_PATH):
        try:
            version_db()
            print(50 * '-')
            print(" WSPR Database Stats")
            print(50 * '-')
            qt1 = time.time()
            with sqlite3.connect(DB_PATH) as conn:
                cur = conn.cursor()
                cur.execute('SELECT * FROM appdata ORDER BY ROWID ASC LIMIT 1')
                for row in cur.fetchall():
                    aut = row[0]
                    cop = row[1]
                    lic = row[2]
                    ver = row[3]
                    cnt = row[4]
                    sta = row[5]
            conn.close()

            qt2 = (time.time() - qt1)
            print(" Database Name .....: %s" % DB_NAME)
            print(" Database Version ..: %s" % ver)
            print(" Author ............: %s" % aut)
            print(" Contact ...........: %s" % cnt)
            print(" Copyright .........: %s" % cop)
            print(" License ...........: %s" % lic)
            print(" Status ............: %s" % sta)
            print(" Execution time ....: %.4f seconds" % qt2)
            print("\n")

        except NameError as err:
            print("Name error: {0}".format(err))
            print("Creating Database..: {}".format(DB_NAME))
            raise
            init_db()
    else:
        init_db()


#------------------------------------------------------------- Database version
def version_db():
    """Get WSPR-Ana Version

    Actions Performedie database
        2. Fetch the appdata version"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM appdata ORDER BY ROWID ASC LIMIT 1')
            for row in cur.fetchall():
                dbv = row[3]
        conn.close()
        return dbv
    except sqlite3.OperationalError as sql3_error:
        print("")
        print(45 * '-')
        print(sql3_error)
        print("There was a problem the DB, performing clean initialization")
        print(45 * '-')
        print("")
        init_db()

#----------------------------------------------------------- MD5SUM csv.gz file
def md5(fname):
    """Inactive Function - ( For Future Development )

    MD5SUM Check File
    Source: http://stackoverflow.com/questions/3431825/

    Actions Performed:
        1. Creates MD5SUM for a file
        2. Returns the hash as a variable"""
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    f.close()
    return hash_md5.hexdigest()


#----------------------------------------------------------- Add CSV data to db
def add_csv_file(value):
    """Inactive Function - ( For Future Development )

    Add Archive File From WSPRnet.org Achieves to Status Table

    Actions Performed:
        1. MD5SUM check archive file
        2. Unpack the file ( zip or gz )
        3. Count columns in the CSV file.
        4. Add data to Status Table

        NOTE: Some versions 13 fields while others have 14 or 15"""
    print("* Database .......: {}".format(DB_NAME))
    csvfile = (APP_DIR + (os.sep) + value)
    fname = (csvfile)
    MD5 = (md5(fname))
    print("* CSV File Name ..: {}".format(os.path.basename(csvfile)))
    print("* CSV MD5 Sum ....: {}".format(MD5))
    csv_lines = sum(1 for line in open(csvfile))
    cvs_lines.close()

    csv_cols = 0
    with open(csvfile) as f:
        reader = csv.reader(f, delimiter=',', skipinitialspace=True)
        first_row = next(reader)
        csv_cols = len(first_row)
        print("* CSV Columns ....: {}".format(csv_cols))
    f.close()

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        data = csv.reader(open(csvfile))

        # early versions of the archive files only have 13 fields
        if csv_cols == 13:
            cur.executemany('''INSERT into records(spot_id,timestamp,reporter,
                            reporter_grid,snr,frequency,call_sign,grid,power,
                            drift,distance,azimuth,band)
                            values (?,?,?,?,?,?,?,?,?,?,?,?,?);''', data)
         # some files have 14 fields
        elif csv_cols == 14:
            cur.executemany('''INSERT into records(spot_id,timestamp,reporter,
                            reporter_grid,snr,frequency,call_sign,grid,power,
                            drift,distance,azimuth,band,version)
                            values (?,?,?,?,?,?,?,?,?,?,?,?,?,?);''', data)
         # current  files have 15 fields
        else:
            cur.executemany('''INSERT into records(spot_id,timestamp,reporter,
                            reporter_grid,snr,frequency,call_sign,grid,power,
                            drift,distance,azimuth,band,version,code)
                            values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);''', data)
        conn.commit()
    conn.close()
    data.close()

    # update the status table
    utime = time.strftime("%Y-%b-%d", time.gmtime())
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute('''REPLACE into status(name,date_added,columns,records)
                    values (?,?,?,?);''', (os.path.basename(csvfile),
                                           utime, csv_cols, csv_lines))
        conn.commit()
    conn.close()

#--------------------------------------------- Remove all .csv files from CSV_PATH
def clean_csv_path():
    """Removes All CSV Files from CSV Directory

    Actions Performed:
        1. Change directory to CSV_PATH
        2. Glob list of csv files
        3. Remove the files
        4. Change back to APP_DIR"""
    os.chdir(CSV_PATH)
    file_list = glob.glob("*.csv")
    for f in file_list:
        os.remove(f)

    os.chdir(APP_DIR)


#-------------------------------------------------------------- Parse html page
def csvf(BASE_URL):
    """Parse wsprnet.org HTML Page and Extracts Archive File Names

    Actions Performed:
        1. Use HTML parser for scrape archive page
        1. Returns a list of available files"""
    list = BeautifulSoup(requests.get(BASE_URL).text, "html.parser")
    for a in list.find_all('a'):
        yield a['href']


#--------------------------------------------------------------- Download Files
def download_files(value):
    """Download WSPRNet Archive Files

    Actions Performed:
        1. Gets archive name from WSPRNet, then downloads the file
        2. Updates the databse via update_status() function"""
    os.chdir(SRC_PATH)
    print("")
    r = requests.get(BASE_URL + value, stream=True)
    with open(value, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for sect in progress.bar(r.iter_content(chunk_size=1024),
                                 label=("* " + value + " "), expected_size=(total_length / 1024) + 1):
            if sect:
                f.write(sect)
                f.flush()
    f.close()

    # now that the file has been downloaded to SRC_PATH, update the status table
    extract_file(value)
    fname = (value)
    utime = time.strftime("%Y-%b-%d", time.gmtime())
    lines = (records)
    columns = (csv_cols)
    
    update_stats(value, utime, columns, lines)
    clean_csv_path()

#------------------------------------------------- Update database status table
def update_stats(value, utime, columns, lines):
    """Update Database Stats Table

    Actions Performed:
        1. Connects to the SQLit3 database
        2. Commits data to status table"""

    # check the DB is OK
    version_db()

    # add the update to database status table
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''REPLACE into status(name,date_added,columns,records)
                values (?,?,?,?);''', (value, utime, columns, lines))
    conn.commit()
    conn.close()


#------------------------------------------------------ Extract monthly archive
def extract_current_month(value):
    src = (SRC_PATH + (os.sep) + value)
    dest_dir = (CSV_PATH)
    dest_name = os.path.join(dest_dir, value[:-3])
    with gzip.open(src, 'rb') as infile:
        with open(dest_name, 'wb') as outfile:
            for line in infile:
                outfile.write(line)
    infile.close()
    outfile.close()


#--------------------------------------------------------- Extract archive file
def extract_file(value):
    """Extract Downloaded Archive Files

    Actions Performed:
        1. Extracts a downloaded archive file
        2. Return files size, csv columns and record count

            Variables: fsize, csv_cols, records"""
    global records
    global csv_cols
    global fsize
    fsize = 0
    csv_cols = 0
    records = 0
    os.chdir(APP_DIR)
    src = (SRC_PATH + (os.sep) + value)
    dest_dir = (CSV_PATH)
    dest_name = os.path.join(dest_dir, value[:-3])
    qt1 = time.time()

    # extract the .zip / .gz file
    print("* Extracting Archive ..: {}".format(value))
    with gzip.open(src, 'rb') as infile, open(dest_name, 'wb') as outfile:
        for line in infile:
            outfile.write(line)

    infile.close()
    outfile.close()
    qt2 = (time.time() - qt1)

    # get the number of columns and records
    # use mmap for speed increa, could also use multi-core processing
    qt3 = time.time()

    # get record count
    with open(dest_name, "r") as f:
        reader = csv.reader(f, delimiter=' ', skipinitialspace=True)
        first_row = next(reader)
        data = list(reader)
        records = len(data)
    f.close()

    # get column cound
    with open(dest_name) as f:
        reader = csv.reader(f, delimiter=',', skipinitialspace=True)
        first_row = next(reader)
        num_cols = len(first_row)
    f.close()
    qt4 = (time.time() - qt3)

    # get the file size before deleting
    fsize = os.stat(dest_name).st_size
    print("* CSV File Name .......: {}".format(value[:-3]))
    print("* CSV Size ............: {:,} bytes".format(fsize))
    print("* CSV Columns .........: {}".format(num_cols))
    print("* CSV Record Count ....: {:,}".format(records))
    print("* Extraction Time .....: %.2f seconds" % qt2)
    print("* Record Query Time ...: %.2f seconds" % qt4)
    return fsize, csv_cols, records
    clean_csv_path()

#--------------------------------------------------------- Check the db archive
def download_all():
    """Check Archive File For Changes

    Actions Performed:
        1. Generates a list of archive files from WSPRNET
        2. Checks the file sizes both local and remote
        3. If Local and Remote do not match, download new archive file"""
    print("\n" + 65 * '-')
    print(" Checking Archives - ( please be patient )")
    print(65 * '-')
    lcount = 0

    # check local and remote file sizes
    for l in csvf(BASE_URL):
        if l.endswith(OS_EXT):

            # get remote file size
            checkurl = (BASE_URL + l)
            req = requests.head(checkurl)
            req.content
            remote_size = (req.headers['content-length'])

            # get local file size
            checkfile = (SRC_PATH + (os.sep) + l)
            if os.path.isfile(checkfile):
                try:
                    local_size = (os.path.getsize(SRC_PATH + (os.sep) + l))
                except:
                    local_size = 0
                    pass
            else:
                local_size = 0

            if (int(remote_size)) != (int(local_size)):
                DWN_LIST.append(l)
            else:
                print("* {} size {:,} bytes is Up To Date".format(l, local_size))

    # check if archive data is missing or different from status table
    for l in csvf(BASE_URL):
        if l.endswith(OS_EXT):
            lcount += 1
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute('SELECT name FROM status WHERE name=?', (l,))
            d = cur.fetchall()
            conn.close()
            if not d:
                DWN_LIST.append(l)

    # print needed updates and run
    ix = len(DWN_LIST)
    print("\n")
    print(45 * '-')
    print(" Archive Summary")
    print(45 * '-')
    print("* Total Archives ..: %s " % lcount)
    print("* Updates Needed ..: %s \n" % ix)
    if ix > 0:
        for value in sorted(DWN_LIST):
            download_files(value)


#---------------------------------------------------- Update current month only
def update_current_month():
    """Download The Latest Monthly Archive File

    Each night (early hours UTC), WSPRNET updates the current monthly archive.
    This function will synchronize the local file against the latest server
    posting.

    Actions Performed:
        1. Checks local and remote file size
        2. If the sizes are different, downloads new archive file

    """
    set_ext()
    y = (time.strftime("%Y"))
    m = (time.strftime("%m"))
    month = (time.strftime("%B"))
    value = ("wsprspots-" + y + "-" + m + ".csv." + OS_EXT)

    # get remote file size
    checkurl = (BASE_URL + value)
    req = requests.head(checkurl)
    req.content
    remote_size = (req.headers['content-length'])

    print("\n" + 45 * '-')
    print(" Updating %s" % value)
    print(45 * '-')

    # download a new archive file if Local and Remote sizes do not match
    checkfile = (SRC_PATH + (os.sep) + value)
    if os.path.isfile(checkfile):
        try:
            local_size = (os.path.getsize(SRC_PATH + (os.sep) + value))
        except:
            local_size = 0
    else:
        local_size = 0

    if (int(remote_size)) != (int(local_size)):
        download_files(value)
    else:
        clear_screen
        r = int(remote_size)
        l = int(local_size)
        print("* File Name ..........: %s" % value)
        print("* Remote File Size ...: {:,} bytes".format(r))
        print("* Local File Size ....: {:,} bytes".format(l))
        print("* Local File Status ..: Up to Date\n")

#--------------------------------------------------------------- Unpack archive
def update_status_table():
    """Update Database Status Table For Each Archive File

    Actions Performed:
        1. Creates a list of downloaded archive files
        2. Loop through all archive files and update database status table
    """
    trecords = 0
    tfsize = 0
    tfcount = 0
    ulist = []
    print("\n" + 45 * '-')
    print(" Updating Table Data - ( please be patient )")
    print(45 * '-')
    ttime1 = time.time()
    total_records = 0
    total_size = 0

    # create the update list
    for fname in os.listdir(SRC_PATH):
        if fname.endswith(OS_EXT):
            ulist.append(fname)

    # loop through each file, get stats, update the database status table
    for value in sorted(ulist):
        extract_file(value)
        fname = (value)
        utime = time.strftime("%Y-%b-%d", time.gmtime())
        lines = (records)
        columns = (csv_cols)
        update_stats(value, utime, columns, lines)
        trecords += records
        tfsize += fsize
        tfcount += 1

    ttime2 = ((time.time() - ttime1) / 60)

    # print the summary
    print("\n" + 45 * '-')
    print(" Status Table Update Summary")
    print(45 * '-')
    print(" * Total Files .......: {:,}".format(tfcount))
    print(" * Total Records .....: {:,}".format(trecords))
    print(" * Total Bytes .......: {:,}".format(tfsize))
    print(" * Processing Time ...: %.1f minutes \n" % ttime2)


#---------------------------------------- Create csv file from all tar.gz files
def search_all_months_for_callsign(call):
    """Search All Archive Files For A Given Callsign

    Original Script by ...: Gian Piero I2GPG
    Re-Written by ........: Greg Beam, KI7MT

    Actions Performed:
        1. Searches ALL downloaded archive files for a given callsign
        2. Creates a .csv file: <call>-<month>-<year>.csv

    """
    # reset timers and prompt user for callsign
    reset_timers()

    # create the output file name and open the file for writing
    mylogfile = REPORTS_PATH + (os.sep) + call + "-all" + ".csv"
    w = open(mylogfile, "w")

    # get the list and count of all archive files
    months = sorted(glob.glob(SRC_PATH + (os.sep) + '*.gz'), key=os.path.basename)
    nmonths = len(months)
    print("\n" + 45 * '-')
    print(" Searching %s Archive Files for [ %s ]" % (str(nmonths), call))
    print(45 * '-')

    # loop through each file and extract lines containing <callsign>
    qt1 = time.time()
    for count in range(nmonths):
        file_name = months[count].split("wsprspots-", 1)[1]
        print("* Processing...: wsprspots-%s " % file_name)
        r = gzip.open(months[count], "r")
        for line in r:
            if call in line:
                # split data fields
                x = line.split(',')
                if (x[2] == call) or (x[6] == call):        # callsign or reporter fields only
                    # decode and replace time stamp
                    s = float(x[1])
                    d = tme.strftime('%Y-%m-%d', time.gmtime(s))
                    t = time.strftime('%H%M', time.gmtime(s))
                    timestamp = str(d) + ',' + str(t)
                    newl = x[0] + ',' + timestamp
                    for count in range(len(x) - 2):                    # copy rest of the line
                        newl = newl + ',' + x[count + 2]
                    # write line to output file
                    w.write(newl,)
    r.close()
    w.close()
    qt2 = ((time.time() - qt1) / 60)
    print("--End of Job--")

    # get total number of entries in <call>-all.csv file
    with open(mylogfile, "r") as f:
        reader = csv.reader(f, delimiter=",")
        data = list(reader)
        ncount = len(data)

    f.close()

    # print job summary data
    print("\n" + 45 * '-')
    print(" Search Summary For [ %s ]" % call)
    print(45 * '-')
    print("* Files Processed ..: %s " % nmonths)
    print("* Log Entry Count ..: %s " % ncount)
    print("* Process Time .....: %.1f minutes" % qt2)
    print("* File Location ....: %s " % mylogfile)


#-------------------------------------------- Search current month for callsign
def search_current_month_for_callsign(callargs):
    """Search Current Month For A Given Callsign

    Original Script by ...: Gian Piero I2GPG
    Modified by ..........: Greg Beam, KI7MT

    Actions Performed:
        1. Updates the current months archive file
        2. Creates a .csv file: <call>-<month>-<year>.csv
    """
    # get date parameters

    now = DATE_TIME.strftime("%Y-%m")
    sdate = DATE_TIME.strftime("%Y-%m-01")
    edate = DATE_TIME.strftime("%Y-%m-%d")

    # create the reports directory ../reports/yyyy-mm-dd
    rpt_dir = (REPORTS_PATH + (os.sep) + edate)
    if not os.path.exists(rpt_dir):
        os.makedirs(rpt_dir)

    # Extrace Zip/GZ file name to search
    gzName = 'wsprspots-' + now + '.csv.' + OS_EXT
    source = (SRC_PATH + (os.sep) + 'wsprspots-' + now + '.csv.' + OS_EXT)
    csvfile = CSV_PATH + (os.sep) + 'wsprspots-' + now + '.csv'

    # Decompress the archive file
    # TO-DO: Make this a generic method for "ALL" and single Archive files
    qt1 = time.time()
    # start processing the source file
    print("\n" + 50 * '-')
    print(" Decompressing Source [ %s ] " % gzName)
    print(50 * '-')
    gzFile = gzip.open(source,"rb")
    ucFile = open(csvfile,"wb")
    decoded = gzFile.read()
    ucFile.write(decoded)
    gzFile.close()
    ucFile.close()
    callcount = 0

    # check callsign args
    for call in callargs:
        try:
            int(call)
        except ValueError:
            callcount += 1

    # loop through each callsign
    for call in callargs:
        print(' Processing .... : %s' % call.upper())
        callfile = rpt_dir + (os.sep) + now + '-' + call.lower() + '-raw' + '.csv'
        call = call.upper()

        # Process the CSV file
        print(" Searching ......: %s " % gzName[:-3])
        search_for = call
        counter = 0
        with open(csvfile) as inf, open(callfile,'w') as outf:
            reader = csv.reader(inf)
            writer = csv.writer(outf)
            for row in reader:
                counter +=1
                sys.stdout.flush()
                if (row[2] == call) or (row[6] == call):
                    writer.writerow(row)
                    print(" Adding Spot Id ( %s )" % counter, end='\r')
            inf.close()
            outf.close()

        # get total number of entries in the new .csv file
        with open(callfile, "r") as f:
            reader = csv.reader(f, delimiter=",")
            data = list(reader)
            ncount = len(data)
        f.close()

        # print the summary
        qt2 = ((time.time() - qt1))
        print(" Process Time ...: %.2f seconds" % qt2)
        print(" Log Count ......: {:,}".format(ncount))
        print(" File Location ..: %s \n" % callfile)


#----------------------------------------------------------- Raw Input Callsign
def enter_callsign():
    """Enter callsign to seach for"""
    global callargs
    print(50 * '-')
    print(" ENTER ONE OR MORE CALLS")
    print(50 * '-')
    msg = """
 You can enter one or more calls separated by ','
 Each call will have its own Raw CSV file.
 
 Example
   Input ....:  KI7MT,XX1XX,ZZ1ZZ
   Creates ..:  <year>-<month>-<call>-raw.csv
                <year>-<month>-<call>-converted.csv
 
 NOTE:  The raw CSV files do not convert epoch time stampes.
        They are extracted exacely as listed in the source
        archive file. This is import for the R scripts
        as they do the epoch conversion automatically.

        To convert the current month CSV file, select the
        feature from the Main Menu.
 """
    print(msg)
    callargs = input(" * Enter Callsigns : ").split(',')
    return callargs


###############################################################################
# USER SUPPLIED REPORT GENERATORS
###############################################################################


#---------------------------------------------------------- Pavel Demin REPORTS_PATH
def pavel_rscripts():
    """Pavel Demin Provides the WSPR Analysis Script written in R
       Source: git clone https://github.com/pavel-demin/wsprspots-analyzer.git
    The following has been constructed to feed each of the three script via
    Python.
    Requirements:
        * R Language base
        * R Packages: ggplot, data-table + Deps
    R Language Installation: (may very depending on distribution)
        # In performed in the Gnome terminal:
        sudo apt-get install r-base r-base-dev  libcurl4-gnutls-dev
        # Actions performed in the R console:
        sudo R
        update.packages()
        install.packages("ggplot2", dependencies=TRUE, repos='http://cran.rstudio.com/'
        install.packages("data.table", dependencies=TRUE, repos='http://cran.rstudio.com/')
        quit("no")
    Function Notes:
        * Generates Graph of WSPR Spots Per Hour Per Band using ggplot
        * Generates Average SNR Different Per Day using ggplot
        * Generates SNR over PWR normalized using ggplot
    Each R script requires 5 variables in the following format
        * Input         file-call.csv               # current monthly archive file
        * Output        file-per-hour-call.png      # output image file
        * Call(s)       KI7MT,K1ABC,K1DEF           # callsign(s) to search in archive
        * Start Date    2016-04-01                  # first day of the current month
        * End Date      2016-01-18                  # current day in the month"""
    # setup variables
    now = DATE_TIME.strftime("%Y-%m")
    sdate = DATE_TIME.strftime("%Y-%m-01")
    edate = DATE_TIME.strftime("%Y-%m-%d")
    arg = []

    # this gets passed to the gz extract script
    value = ("wsprspots-" + now + ".csv." + OS_EXT)
    srccsv = (CSV_PATH + (os.sep) + 'wsprspots-' + now + '.csv')

    # create the reports directory ../reports/yyyy-mm-dd
    rpt_dir = (REPORTS_PATH + (os.sep) + edate)
    if not os.path.exists(rpt_dir):
        os.makedirs(rpt_dir)
    
    print("\n" + 45 * '-')
    print(" Pavel Demin's R-Script Report Generator")
    print(45 * '-')
    print(" * Separate Calls with a ',' example: KI7MT,K1ABC,K1DEF")
    callargs = input(" * Enter Callsigns : ").split(',')
    callcount = 0

    # used for snr-diff ( not implemented yet )
    for call in callargs:
        try:
            int(call)
        except ValueError:
            callcount += 1
    #print(" * Processing [ %s ] call(s)" % callcount)
    # loop through the calls and call the R script
    for call in callargs:
        call = call.upper()
        # search_current_month_no_split(call)
        mylogfile = rpt_dir + (os.sep) + now + '-' + call.lower() + '-raw.csv'
        arg1 = (mylogfile)
        arg3 = call
        arg4 = sdate
        arg5 = edate
        os.chdir(R_SCRIPT_PATH)

        # script 1
        print(" * Generate Spots Per Hour Plot for [ %s ]" % call)
        scr1 = (rpt_dir + (os.sep) + 'wsprspots-per-hour-' + call.lower() + '.png')
        args = (arg1 + ' ' + scr1 + ' ' + arg3 + ' ' + arg4 + ' ' + arg5)
        with open(os.devnull) as devnull:
            if os.path.isfile(mylogfile):
                subprocess.call(
                    "Rscript wsprspots-per-hour.r " + args,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=devnull)
            else:
                print("   [ %s] Missing CSV. Please generate from the main menu." % call.upper())
        # script 2 ( Not Implemented Yet )
        # print(" * Generate Report ..: SNR DIFF")
        # scr2 = (REPORTS_PATH + (os.sep) + 'wsprspots-snr-diff-' + call + '.png')
        # args = (arg1 + ' ' + scr2 + ' ' + arg3 + ' ' + arg4 + ' ' + arg5)
        # subprocess.call("Rscript wsprspots-snr-diff.r " + args, shell=True)

        # script 3 ( Not Implemented Yet )
        #print(" * Report ......: SNR Normal")
        #scr3 = (REPORTS_PATH + (os.sep) + 'wsprspots-snr-norm-' + call + '.png')
        #args = (arg1 + ' ' + scr3 + ' ' + arg3 + ' ' + arg4 + ' ' + arg5)
        #with open(os.devnull) as devnull:
        #    subprocess.call(
        #        "Rscript wsprspots-snr-norm.r " + args,
        #        shell=True,
        #        stdout=subprocess.PIPE)

    pause()
    return


#---------------------------------------------------------- Main Menu Functions
def main():
    """Main Menu Functions

    Function Notes:
        * Creates required directories
        * Sets the archive file extension based on the platform
        * After each action the CSV_PATH directory is cleaned
        * The pause statement sets up return to main menu

    Option Notes:
        1. Download All WSPRnet Archive Files
        2. Update Current Months Archive File
        3. Search All Archive for Callsign
        4. Seach Current Month for Callsign
        5. Reports Menu
        6. Update DB Status
        7. Clean CSV Directory
        8. Exit

        NOTE: Entries must match the items in print_menu() function.
    """
    
    # make sure directories exist
    create_dirs()

    # check that wsprana database exists
    version_db()
    
    # set the archive extension
    set_ext()

    # start main loop
    clear_screen()
    while True:
        main_menu()
        selection = input("Selection: ")
        # update all archive files from WSPRnet
        if selection == '1':
            download_all()
            pause()
            menu()
        # search all archives for call
        if selection == '2':
            under_development()
            #enter_callsign()
            #search_all_months_for_callsign(call)
            pause()
            main()
        # update current month from WSPRnet
        if selection == '3':
            update_current_month()
            pause()
            main()
        # search current month for a call
        if selection == '4':
            clear_screen()
            enter_callsign()
            search_current_month_for_callsign(callargs)
            pause()
            main()

        # search current month for a call
        if selection == '5':
            clear_screen()
            enter_callsign()
            now = DATE_TIME.strftime("%Y-%m")
            edate = DATE_TIME.strftime("%Y-%m-%d")
            for call in callargs:
                csv_in = REPORTS_PATH + (os.sep) + edate + (os.sep) + now + '-' + call.lower() + '-raw.csv'
                csv_out = REPORTS_PATH + (os.sep) + edate + (os.sep) + now + '-' + call.lower() + '-converted.csv'
                ut.convert_epoch_lines(call,csv_in,csv_out)
            os.chdir(BASE_PATH)
            pause()
            main()

        # List available reports
        if selection == '6':
            report_selection()
        # Check database
        if selection == '7':
            check_db()
            pause()
            main()
        # Clean up csvd directory, removes all csv files
        if selection == '8':
            afiles = len(glob.glob1(CSV_PATH, "*.csv"))
            print("\n" + 45 * '-')
            print(" Cleanup CSV Directory")
            print(45 * '-')
            if afiles == 0:
                print(" * CSV Directory Is Clean, Nothing To Be Done \n")
            else:
                print(" * Removing [ %s ] files from CSV Directory" % afiles)
                clean_csv_path()
                print(" * Finished Cleanup")

            pause()
            main()
        # Exit the menu
        if selection == '9':
            sys.exit("\n")

        else:
            return


#---------------------------------------------------------- Main Menu Functions
def report_selection():
    """Report Functions"""
    clear_screen()
    while True:
        report_menu()
        selection = input("Selection: ")

        if selection == '1':
            pavel_rscripts()

        if selection == '2':
            main()

        if selection == '3':
            sys.exit("\n")

        else:
            report_menu()


#-------------------------------------------------------------------- Main Menu
def main_menu():
    """Prints The Main Menu"""
    cmon = DATE_TIME.strftime("%B")
    print(45 * "-")
    print(" WSPR Analysis Main Menu")
    print(45 * "-")
    print("\n ALL ARCHIVE FUNCTIONS")    
    print("   1. Update All Archive Files")
    print("   2. Search All Archives for Call")
    print("\n CURRENT MONTH FUNCTIONS - [ %s ]" % cmon)    
    print("   3. Update Archive")
    print("   4. Search Archive For Call")
    print("   5. Convert raw csv from epoch")
    print("\n REPORT FUNCTIONS")
    print("   6. Reports Menu")
    print("\n UTILITIES")    
    print("   7. Check Database")
    print("   8. Clean CSV Directory")
    print("   9. Exit")
    print("")


#------------------------------------------------------------------ Report Menu
def report_menu():
    """Prints The Report menu"""
    clear_screen()
    cmon = DATE_TIME.strftime("%B")
    print(45 * "-")
    print(" WSPR Analysis Report Menu")
    print(45 * "-")
    print(" 1. Spots Per Hour Report ( last 24hrs )")
    print(" 2. Back To Main Menu")
    print(" 3. Exit")
    print("")

if __name__ == "__main__":
    create_dirs()
    main()

# END WSPR-Ana
