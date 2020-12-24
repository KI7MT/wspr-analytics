#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
import os
import sqlite3
import subprocess
import sys
import time
from builtins import input
from os.path import expanduser

import requests
from bs4 import BeautifulSoup
from clint.textui import progress

from . import __title__
from . import utils as ut

home_dir = expanduser("~")
"""User home directory for Linux: /home/$USER"""

if os.name == 'nt':
    wsprana_share = os.path.join(os.environ['LOCALAPPDATA'], __title__)
else:
    wsprana_share = os.path.join(home_dir, '.local', 'share', __title__)
r"""
    User share directory
        Linux: /home/$USER/share
        MacOS: /Users/$USER/share
        Win32: C:\Users\%USERNAME%\AppData\local\wsprana
"""

if os.name == 'nt':
    wsprana_config = wsprana_share
else:
    wsprana_config = os.path.join(home_dir, '.config', __title__)
r"""
    User share directory: /home/$USER/.config/wsprana
        Linux: /home/$USER/share/wsprana
        MacOS: /Users/$USER/share/wsprana
        Win32: C:\Users\%USERNAME%\AppData\local\wsprana
"""

csv_dir = os.path.join(wsprana_share, 'csvd')
r"""
    CSV share for access to decompressed files
        Linux: /home/$USER/.local/share/wsprana/csvd
        MacOS: /Users/$USER/.local/share/wsprana/csvd
        Win32: C:\Users\%USERNAME%\AppData\local\wsprana\csvd
"""

src_dir = os.path.join(wsprana_share, 'srcd')
r"""
    SRCD path for downloaded files
        Linux: /home/$USER/.local/share/wsprana/srcd
        MacOS: /Users/$USER/.local/share/wsprana/srcd
        Win32: C:\Users\%USERNAME%\AppData\local\wsprana\srcd
"""

parquet_dir = os.path.join(wsprana_share, 'parquet')
r"""
    Parquest share for converted parquet files
        Linux: /home/$USER/.local/share/wsprana/parquet
        MacOS: /Users/$USER/.local/share/wsprana/parquet
        Win32: C:\Users\%USERNAME%\AppData\local\wsprana\parquet
"""

reports_dir = os.path.join(wsprana_share, 'reports')
r"""
    Folder for 
        Linux: /home/$USER/.local/share/wsprana/parquet
        MacOS: /Users/$USER/.local/share/wsprana/parquet
        Win32: C:\Users\%USERNAME%\AppData\local\wsprana\parquet
"""

__sqldir__ = os.path.join(
                os.path.dirname(
                    os.path.abspath(__file__)), 'resources/sql')
"""Path to sql scripts after install"""

__rscripts__ = os.path.join(
                os.path.dirname(
                    os.path.abspath(__file__)), 'resources/rscripts')
"""Path to R scripts after instasll"""

db_name = __title__+'.db'
"""The `database name`"""

db_path = os.path.join(wsprana_share, 'wsprana.db')
"""Path and name to wsprana database"""

sql_file = os.path.join(__sqldir__, 'wsprana.sql')
"""DB init sql script"""

# general variables
dir_list = [csv_dir, src_dir, parquet_dir, reports_dir]


date_time = datetime.date.today()
dwn_list = []
BASE_URL = "http://wsprnet.org/archive/"
OS_EXT = ''


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
    copy them to the src_dir directory after cloning.

        1. git clone git://git.code.sf.net/u/ki7mt/wspr-ana
        2. Copy previously downloaded WSPRNet archive files to ./wspr-ana/src_dir
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

        src_dir ......: Directory for WSPRNet archive files
        csv_dir ......: Directory for extracted csv files
        reports_dir ..: Directory for output files
        wsprana .......: SQLite3 Database
        sql_file ......: SQL template for pre-loading the database
        wsprana.py ....: Main script


     DEFAULT DATABASE:

     A default database, updated as of the latest git posting, is provided in
     the repository. The data contained in the [ status ] table contains the
     following fields:

     name ......: archive file name from WSPRNet
     date ......: the date the status was last updated
     column ....: the number of columns for the archive file
     records ...: the number of records in the archive .csv file"""


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


def create_dirs():
    """Create Script Directories

    Actions Performed:
        1. Creates directories if they do no exist"""
    for d in dir_list:
        if not os.path.exists(d):
            os.makedirs(d)


def reset_timers():
    """Reset Timer Values

    Actions Performed:
        1. Resets timers used in various functions"""
    # qt1 = 0  # pylint: disable=unused-variable
    # qt2 = 0  # pylint: disable=unused-variable
    # qt3 = 0  # pylint: disable=unused-variable
    # qt4 = 0  # pylint: disable=unused-variable
    # qt5 = 0  # pylint: disable=unused-variable
    # qt6 = 0  # pylint: disable=unused-variable
    # qt7 = 0  # pylint: disable=unused-variable
    # qt8 = 0  # pylint: disable=unused-variable
    # qt9 = 0  # pylint: disable=unused-variable
    # qt10 = 0  # pylint: disable=unused-variable


def clear_screen():
    """Clear Screen Based On Platform Type

    Actions Performed:
        1. Is Platform is Windows, use 'cls'
        2. Is Platform is Windows, use 'clear'"""
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')


def pause():
    """Pause Statement

    Actions Performed:
        1. Prompt the user for input to create a pause"""
    input("\nPress [ ENTER ] to continue...")


def under_development():
    print("\n" + 45 * '-')
    print(" Under Development")
    print(45 * '-')
    print("\n This feature is currently under development.")
    print("")


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
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        fd = open(sql_file, 'r')
        script = fd.read()
        cur.executescript(script)
        fd.close()

        cur.execute('SELECT SQLITE_VERSION()')
        sv = cur.fetchone()

        cur.execute('''SELECT * FROM appdata ORDER BY ROWID ASC LIMIT 1''')
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
    print(" Database Name .....: %s" % db_name)
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


def check_db():
    """Check Database Connection

    Actions Performed:
        1. Connect to database via the db_path() function
        2. If the database does not exist, create it with init_db()"""
    if os.path.isfile(db_path):
        try:
            version_db()
            print(50 * '-')
            print(" WSPR Database Stats")
            print(50 * '-')
            qt1 = time.time()
            with sqlite3.connect(db_path) as conn:
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
            print(" Database Name .....: %s" % db_name)
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
            print("Creating Database..: {}".format(db_name))
            raise
    else:
        init_db()


def version_db():
    """Get WSPR-Ana Version

    Actions Performedie database
        2. Fetch the appdata version"""
    try:
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            cur.execute('''SELECT * FROM appdata ORDER BY ROWID ASC LIMIT 1''')
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


def add_csv_file(value):
    """Inactive Function - ( For Future Development )

    Add Archive File From WSPRnet.org Achieves to Status Table

    Actions Performed:
        1. MD5SUM check archive file
        2. Unpack the file ( zip or gz )
        3. Count columns in the CSV file.
        4. Add data to Status Table

        NOTE: Some versions 13 fields while others have 14 or 15"""
    print("* Database .......: {}".format(db_name))
    csvfile = (csv_dir + os.sep + value)
    fname = (csvfile)
    MD5 = (md5(fname))
    print("* CSV File Name ..: {}".format(os.path.basename(csvfile)))
    print("* CSV MD5 Sum ....: {}".format(MD5))
    csv_lines = sum(1 for line in open(csvfile))

    csv_cols = 0
    with open(csvfile) as f:
        reader = csv.reader(f, delimiter=',', skipinitialspace=True)
        first_row = next(reader)
        csv_cols = len(first_row)
        print("* CSV Columns ....: {}".format(csv_cols))
    f.close()

    with sqlite3.connect(db_path) as conn:
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
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute('''REPLACE into status(name,date_added,columns,records)
                    values (?,?,?,?);''', (os.path.basename(csvfile),
                                           utime, csv_cols, csv_lines))
        conn.commit()
    conn.close()


def clean_csv_dir():
    """Removes All CSV Files from CSV Directory

    Actions Performed:
        1. Change directory to csv_dir
        2. Glob list of csv files
        3. Remove the files
        4. Change back to APP_DIR"""
    os.chdir(csv_dir)
    file_list = glob.glob("*.csv")
    for f in file_list:
        os.remove(f)

    os.chdir(wsprana_share)


def csvf(BASE_URL):
    """Parse wsprnet.org HTML Page and Extracts Archive File Names

    Actions Performed:
        1. Use HTML parser for scrape archive page
        1. Returns a list of available files"""
    list = BeautifulSoup(requests.get(BASE_URL).text, "html.parser")
    for a in list.find_all('a'):
        yield a['href']


def download_files(value):
    """Download WSPRNet Archive Files

    Actions Performed:
        1. Gets archive name from WSPRNet, then downloads the file
        2. Updates the database via update_status() function"""
    os.chdir(src_dir)
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

    # now that the file has been downloaded to src_dir, update the status table
    extract_file(value)
    fname = (value)
    utime = time.strftime("%Y-%b-%d", time.gmtime())
    lines = (records)
    columns = (csv_cols)

    update_stats(value, utime, columns, lines)
    clean_csv_dir()


def update_stats(value, utime, columns, lines):
    """Update Database Stats Table

    Actions Performed:
        1. Connects to the SQLit3 database
        2. Commits data to status table"""

    # check the DB is OK
    version_db()

    # add the update to database status table
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('''REPLACE into status(name,date_added,columns,records)
                values (?,?,?,?);''', (value, utime, columns, lines))
    conn.commit()
    conn.close()


def extract_current_month(value):
    src = (src_dir + os.sep + value)
    dest_dir = (csv_dir)
    dest_name = os.path.join(dest_dir, value[:-3])
    with gzip.open(src, 'rb') as infile:
        with open(dest_name, 'wb') as outfile:
            for line in infile:
                outfile.write(line)
    infile.close()
    outfile.close()


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
    os.chdir(src_dir)
    src = (src_dir + os.sep + value)
    dest_dir = (csv_dir)
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
    clean_csv_dir()


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
            checkfile = (src_dir + os.sep + l)
            if os.path.isfile(checkfile):
                try:
                    local_size = (os.path.getsize(src_dir + os.sep + l))
                except:
                    local_size = 0
                    pass
            else:
                local_size = 0

            if (int(remote_size)) != (int(local_size)):
                dwn_list.append(l)
            else:
                print("* {} size {:,} bytes is Up To Date".format(l, local_size))

    # check if archive data is missing or different from status table
    for l in csvf(BASE_URL):
        if l.endswith(OS_EXT):
            lcount += 1
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute('SELECT name FROM status WHERE name=?', (l,))
            d = cur.fetchall()
            conn.close()
            if not d:
                dwn_list.append(l)

    # print needed updates and run
    ix = len(dwn_list)
    print("\n")
    print(45 * '-')
    print(" Archive Summary")
    print(45 * '-')
    print("* Total Archives ..: %s " % lcount)
    print("* Updates Needed ..: %s \n" % ix)
    if ix > 0:
        for value in sorted(dwn_list):
            download_files(value)


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
    checkfile = (src_dir + os.sep + value)
    if os.path.isfile(checkfile):
        try:
            local_size = (os.path.getsize(src_dir + os.sep + value))
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
    for fname in os.listdir(src_dir):
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
    mylogfile = reports_dir + os.sep + call + "-all" + ".csv"
    w = open(mylogfile, "w")

    # get the list and count of all archive files
    months = sorted(glob.glob(src_dir + os.sep + '*.gz'), key=os.path.basename)
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
                if (x[2] == call) or (x[6] == call):  # callsign or reporter fields only
                    # decode and replace time stamp
                    s = float(x[1])
                    d = time.strftime('%Y-%m-%d', time.gmtime(s))
                    t = time.strftime('%H%M', time.gmtime(s))
                    timestamp = str(d) + ',' + str(t)
                    newl = x[0] + ',' + timestamp
                    for count in range(len(x) - 2):  # copy rest of the line
                        newl = newl + ',' + x[count + 2]
                    # write line to output file
                    w.write(newl, )
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


def search_current_month_for_callsign(callargs):
    """Search Current Month For A Given Callsign

    Original Script by ...: Gian Piero I2GPG
    Modified by ..........: Greg Beam, KI7MT

    Actions Performed:
        1. Updates the current months archive file
        2. Creates a .csv file: <call>-<month>-<year>.csv
    """
    # get date parameters

    now = date_time.strftime("%Y-%m")
    sdate = date_time.strftime("%Y-%m-01")
    edate = date_time.strftime("%Y-%m-%d")

    # create the reports directory ../reports/yyyy-mm-dd
    rpt_dir = (reports_dir + os.sep + edate)
    if not os.path.exists(rpt_dir):
        os.makedirs(rpt_dir)

    # Extrace Zip/GZ file name to search
    gzName = 'wsprspots-' + now + '.csv.' + OS_EXT
    source = (src_dir + os.sep + 'wsprspots-' + now + '.csv.' + OS_EXT)
    csvfile = csv_dir + os.sep + 'wsprspots-' + now + '.csv'

    # Decompress the archive file
    # TO-DO: Make this a generic method for "ALL" and single Archive files
    qt1 = time.time()
    # start processing the source file
    print("\n" + 50 * '-')
    print(" Decompressing Source [ %s ] " % gzName)
    print(50 * '-')
    gzFile = gzip.open(source, "rb")
    ucFile = open(csvfile, "wb")
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
        callfile = rpt_dir + os.sep + now + '-' + call.lower() + '-raw' + '.csv'
        call = call.upper()

        # Process the CSV file
        print(" Searching ......: %s " % gzName[:-3])
        search_for = call
        counter = 0
        with open(csvfile) as inf, open(callfile, 'w') as outf:
            reader = csv.reader(inf)
            writer = csv.writer(outf)
            for row in reader:
                counter += 1
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


def main():
    """Main Menu Functions

    Function Notes:
        * Creates required directories
        * Sets the archive file extension based on the platform
        * After each action the csv_dir directory is cleaned
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
            main_menu()
        # search all archives for call
        if selection == '2':
            under_development()
            # enter_callsign()
            # search_all_months_for_callsign(call)
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
            now = date_time.strftime("%Y-%m")
            edate = date_time.strftime("%Y-%m-%d")
            for call in callargs:
                csv_in = reports_dir + os.sep + edate + os.sep + now + '-' + call.lower() + '-raw.csv'
                csv_out = reports_dir + os.sep + edate + os.sep + now + '-' + call.lower() + '-converted.csv'
                ut.convert_epoch_lines(call, csv_in, csv_out)
            os.chdir(home_dir)
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
            afiles = len(glob.glob1(csv_dir, "*.csv"))
            print("\n" + 45 * '-')
            print(" Cleanup CSV Directory")
            print(45 * '-')
            if afiles == 0:
                print(" * CSV Directory Is Clean, Nothing To Be Done \n")
            else:
                print(" * Removing [ %s ] files from CSV Directory" % afiles)
                clean_csv_dir()
                print(" * Finished Cleanup")

            pause()
            main()
        # Exit the menu
        if selection == '9':
            sys.exit("\n")

        else:
            return


def report_selection():
    """Report Functions"""
    clear_screen()
    while True:
        report_menu()
        selection = input("Selection: ")

        if selection == '1':
            pause()
            main()
            #pavel_rscripts()

        if selection == '2':
            main()

        if selection == '3':
            sys.exit("\n")

        else:
            report_menu()


def main_menu():
    """Prints The Main Menu"""
    cmon = date_time.strftime("%B")
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


def report_menu():
    """Prints The Report menu"""
    clear_screen()
    date_time.strftime("%B")
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
