#!/usr/bin/env python

from __future__ import print_function

###############################################################################
#    wsprdb.py
#
#    Copyright 2016 Greg Beam <ki7mt@yahoo.com>
#    Copyright 2016 Gian Piero I2GPG <i2gpg@wedidit.it> 
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; Version 3 of the License
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, the license can be downloaded here:
#
#    http://www.gnu.org/licenses/gpl.html
#
###############################################################################


#--------------------------------------------------------------- import mudules
import os
import sys
import time
import datetime
import csv
import sqlite3
import readline
import hashlib
import gzip
import glob
import mmap
import requests
from clint.textui import progress
from bs4 import BeautifulSoup
from time import gmtime

#-------------------------------------------------------------------- meta data
__author__ = 'Greg Beam' 
__copyright__ = 'GPLv3'
__version__ = '1.0.0'
__version_info__ = (1, 0, 0)
__email__ = '<ki7mt@yahoo.com>'
__status__ = 'Development'
__license__ = "GNU General Public License (GPL) Version 3"


#--------------------------------------------------- global variables and paths
appdir = os.getcwd()
srcd = (appdir + (os.sep) + 'srcd')
csvd = (appdir + (os.sep) + "csvd")
reports = (appdir + (os.sep) + "reports")
dbname = 'wsprana.db'
dbf = (appdir + (os.sep) + dbname)
dirs=['srcd', 'csvd', 'reports']
sqlf = ("wsprdb.sql")
Url = "http://wsprnet.org/archive/"
dwn_list=[]
today = datetime.date.today()


#------------------------------------------------------ Help and Docstring Data
def a_help():
    """WSPRDB Help and General Information
    
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
    copy them to the srcd directory after clonning.

        1. git clone git://git.code.sf.net/u/ki7mt/wsprdb
        2. Copy previously downloaded WSPRNet archive files to ./wsprdb/srcd
        3. To run, type: ./wsprdb.py
        4. For the first run, select Option-1 to sync archive files
        5. After initial database sync, you can search all or the current
           month for a given callsign.


     OVERVIEW:
     
     WsprDB provides a set of commonly used functions to download and parse
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
               
        srcd .......: Directory for WSPRNet archive files
        csvd .......: Directory for extracted csv files
        reports ....: Directory for output files
        wsprana ....: SQLite3 Database
        sqlf .......: SQL template for pre-loading the database
        wsprdb.py ..: Main script


     DEFAULT DATABASE:

     A default database, updated as of the latest git posting, is provided in
     the repository. The data contained in the [ status ] table contains the
     following fields:
     
     name ......: archive file name from WSPRNet
     date ......: the date the status was last updated
     column ....: the number of columns for the archive file
     records ...: the number of records in the archive .csv file

    """


#----------------------------------------------------------- Set file extension
def set_ext():
    """Set Archive File Extension

    Actions Performed:
        1. For Windows, the extension is set to (zip)
        2. For Linux, the extension is set to (gz)

    """
    global ext
    if sys.platform == "win32":
        ext = "zip"
    else:
        ext = "gz"

    return ext

#----------------------------------------------------------- Create directories
def create_dirs():
    """Create Script Directories

    Actions Performed:
        1. Creates directories if they do no exist

    """
    for z in dirs:
        d=(appdir + (os.sep) + z)
        if not os.path.exists(d):
            os.mkdir(d)


#----------------------------------------------------------------- Reset timers
def reset_timers():
    """Reset Timer Values
    
    Actions Performed:
        1. Resets timers used in various functions

    """
    qt1 = 0
    qt2 = 0
    qt3 = 0
    qt4 = 0
    qt5 = 0
    qt6 = 0
    qt7 = 0
    qt8 = 0
    qt9 = 0
    qt10 = 0

#----------------------------------------------------------------- Clean Screen
def clear_screen():
    """Clear Screen Based On Platform Type
    
    Actions Performed:
        1. Is Platform is Windows, use "cls"
        2. Is Platform is Windows, use "clear"

    """
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')

#--------------------------------------------------------------- Pause function
def pause():
    """Pause Statement
    
    Actions Performed:
        1. Prompt the user for input to create a pause
    
    """    
    raw_input("\nPress <ENTER> for main menu...")


#---------------------------------------------------------- Initialize Database
def init_db():
    """Create Main Database
    
    Actions Performed:
        1. Open SQLit3 Database connection
        2. Execute SQL query to create tables
        3. Add script information to appdata table
        3. Print creation summary
    
    """
    qt1 = time.time()
    print( 50 * '-')
    print("Creating New WSPR Analysis Database")
    print( 50 * '-')

    # connect to SQLite3 database
    with sqlite3.connect(dbf) as conn:
        cur = conn.cursor()
        fd = open(sqlf, 'r')
        script = fd.read()
        cur.executescript(script)
        fd.close()
        
        cur.execute('SELECT SQLITE_VERSION()')
        sv = cur.fetchone()
 
        # default values
        author = (__author__)
        copyright = (__copyright__)
        license = (__license__)
        version = (__version__)
        email = (__email__)
        status = (__status__)
        cur.execute('''INSERT INTO appdata(author,copyright,license,version,email,status) VALUES (?,?,?,?,?,?)''', (author,copyright,license,version,email,status))
        conn.commit()
 
        cur.execute('SELECT * FROM appdata ORDER BY ROWID ASC LIMIT 1')
        for row in cur.fetchall():
            aut=row[0]
            cop=row[1]
            lic=row[2]
            ver=row[3]
            cnt=row[4]
            sta=row[5]

    conn.close()

    qt2 = (time.time()-qt1)
    print(" SQLite Version ....: %s" % sv)
    print(" Database Name .....: %s" % dbname)
    print(" Database Version ..: %s" % ver)
    print(" Author ............: %s" % aut)
    print(" Contact ...........: %s" % cnt)
    print(" Copyright .........: %s" % cop)
    print(" License ...........: %s" % lic)
    print(" Status ............: %s" % sta)
    print(" Execution time ....: %.3f seconds" % qt2)
    print("\n")
    conn.close()


#------------------------------------------------------------ Get database info
def check_db():
    """Check Database Connection
    
    Actions Performed:
        1. Connect to database via the dbf() function
        2. If the database does not exist, create it with init_db()

    """
    if os.path.isfile(dbf):
        try:
            version_db()
            print( 50 * '-')
            print(" WSPR Database Stats")
            print( 50 * '-')
            qt1 = time.time()
            with sqlite3.connect(dbf) as conn:
                cur = conn.cursor()
                cur.execute('SELECT * FROM appdata ORDER BY ROWID ASC LIMIT 1')
                for row in cur.fetchall():
                    aut=row[0]
                    cop=row[1]
                    lic=row[2]
                    ver=row[3]
                    cnt=row[4]
                    sta=row[5]
            conn.close()

            qt2 = (time.time()-qt1)
            print(" Database Name .....: %s" % dbname)
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
            print("Creating Database..: {}".format(dbname))
            raise
            init_db()
    else:
        init_db()


#------------------------------------------------------------- Database version
def version_db():
    """Get WSPRDB Version
    
    Actions Performed
        1. Opens the database
        2. Fetch the appdata version
    
    """
    with sqlite3.connect(dbf) as conn:
        cur = conn.cursor()    
        cur.execute('SELECT * FROM appdata ORDER BY ROWID ASC LIMIT 1')
        for row in cur.fetchall():
            dbv = row[3]
    
    conn.close()
    return dbv


#----------------------------------------------------------- MD5SUM csv.gz file
def md5(fname):
    """Inactive Function - ( For Future Development )
    
    MD5SUM Check File
    Source: http://stackoverflow.com/questions/3431825/    
    
    Actions Performed:
        1. Creates MD5SUM for a file
        2. Returns the hash as a variable
    
    """
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
        
        NOTE: Some versions 13 fields while others have 14 or 15

    """
    print("* Database .......: {}".format(dbname))
    csvfile = (appdir + (os.sep) + value)
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

    with sqlite3.connect(dbf) as conn:
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
    utime = time.strftime("%Y-%b-%d",time.gmtime())
    with sqlite3.connect(dbf) as conn:
        cur = conn.cursor()
        cur.execute('''REPLACE into status(name,date_added,columns,records)
                    values (?,?,?,?);''', (os.path.basename(csvfile), 
                    utime,csv_cols,csv_lines))
        conn.commit()
    conn.close()

    # now cleanup the csv directory
    clean_csvd()


#--------------------------------------------- Remove all .csv files from csvd
def clean_csvd():
    """Removes All CSV Files from CSV Directory
    
    Actions Performed:
        1. Change directory to csvd to csvd
        2. Glob list of csv files
        3. Remove the files
        4. Change back to appdir
    
    """
    os.chdir(csvd)
    file_list = glob.glob("*.csv")
    for f in file_list:
        os.remove(f)
    
    os.chdir(appdir)

#-------------------------------------------------------------- Parse html page
def csvf(Url):
    """Parse wsprnet.org HTML Page and Extracts Archive File Names
    
    Actions Performed:
        1. Use HTML parser for scrape archive page
        1. Returns a list of available files
    
    """
    list = BeautifulSoup(requests.get(Url).text, "html.parser")
    for a in list.find_all('a'):
        yield a['href']


#--------------------------------------------------------------- Download Files
def download_files(value):
    """Download WSPRNet Archive Files

    Actions Performed:
        1. Gets archive name from WSPRNet, then downloads the file
        2. Updates the databse via update_status() function

    """
    os.chdir(srcd)
    r = requests.get(Url + value, stream=True)
    with open(value, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for sect in progress.bar(r.iter_content(chunk_size=1024), 
            label=("* " + value + " "), expected_size=(total_length/1024) + 1):
            if sect:
                f.write(sect)
                f.flush()
    f.close()

    # now that the file has been downloaded to SRCD, update the status table
    extract_file(value)
    fname = (value)
    utime = time.strftime("%Y-%b-%d",time.gmtime())
    lines = (records)
    columns = (csv_cols)
    update_stats(value,utime,columns,lines)

    # cleanup csvd directory
    clean_csvd()


#------------------------------------------------- Update database status table
def update_stats(value,utime,columns,lines):
    """Update Database Stats Table

    Actions Performed:
        1. Connects to the SQLit3 database
        2. Commits data to status table
    
    """
    conn = sqlite3.connect(dbf)
    cur = conn.cursor()
    cur.execute('''REPLACE into status(name,date_added,columns,records)
                values (?,?,?,?);''', (value,utime,columns,lines))
    conn.commit()
    conn.close()


#--------------------------------------------------------- Extract archive file
def extract_file(value):
    """Extract Downloaded Archive Files
    
    Actions Performed:
        1. Extracts a downloaded archive file
        2. Return files size, csv columns and record count
            
            Variables: fsize, csv_cols, records
    
    """
    global records
    global csv_cols
    global fsize
    fsize=0
    csv_cols=0
    records=0
    os.chdir(appdir)
    src = (srcd + (os.sep) + value)
    dest_dir = (csvd)
    dest_name = os.path.join(dest_dir, value[:-3])
    qt1 = time.time()

    # extract the .zip / .gz file
    print("* Extracting Archive ..: {}".format(value))
    with gzip.open(src, 'rb') as infile:
        with open(dest_name, 'wb') as outfile:
            for line in infile:
                outfile.write(line)
    infile.close()
    outfile.close()
    qt2 = (time.time()-qt1)    

    # get the number of columns and records
    # use mmap for speed increa, could also use multi-core processing
    qt3 = time.time()
    with open(dest_name, 'rt', os.O_RDONLY) as f:
        try:
            mInput = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
            L=0
            for s in iter(mInput.readline, ""):
                L+=1            
            records=(int(L))

            qt4 = (time.time()-qt3)   
            mInput.close()
            f.close()

            qt5 = time.time()
            with open(dest_name, 'rt') as f:
                reader = csv.reader(f, delimiter=',', skipinitialspace=True)
                csv_cols = len(reader.next())
            qt6 = (time.time()-qt5)   
            f.close()

            # get the file size before deleting
            fsize = os.stat(dest_name).st_size
            print("* CSV File Name .......: {}".format(value[:-3]))
            print("* CSV Size ............: {:,} bytes".format(fsize))
            print("* CSV Columns .........: {}".format(csv_cols))
            print("* CSV Record Count ....: {:,}".format(records))
            print("* Extraction Time .....: %.4f seconds" % qt2)
            print("* Record Query Time ...: %.4f seconds" % qt4)
            print("* Col Query Time ......: %.4f seconds\n" % qt6)
            return fsize, csv_cols, records

        except ValueError:
            print("* CSV File Is Empty ...: {} \n".format(value[:-3]))

    # clean csvd directory
    clean_csvd()


#--------------------------------------------------------- Check the db archive
def check_archive():
    """Check Archive File For Changes
    
    Actions Performed:
        1. Generates a list of archive files from WSPRNET
        2. Checks the file sizes both local and remote
        3. If Local and Remote do not match, download new archive file
    
    """
    print("\n" + 65 * '-')
    print(" Checking Archives - ( please be patient )")
    print(65 * '-')
    lcount=0

    # check local and remote file sizes
    for l in csvf(Url):
        if l.endswith(ext):
  
            # get remote file size
            checkurl=(Url + l)
            req = requests.head(checkurl)
            req.content
            remote_size=(req.headers['content-length'])

            # get local file size
            checkfile=(srcd + (os.sep) + l)
            if os.path.isfile(checkfile):
                try:
                    local_size=(os.path.getsize(srcd + (os.sep) + l))
                except:
                    local_size = 0
                    pass
            else:
                local_size = 0
            
            if not (int(remote_size)) == (int(local_size)):
                dwn_list.append(l)
            else:
                print("* {} size {:,} bytes is Up To Date".format(l,local_size))
                
    # check if archive data is missing or different from status table
    for l in csvf(Url):
        if l.endswith(ext):
            lcount += 1
            conn = sqlite3.connect(dbf)
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

    # cleanup csvd directory
    clean_csvd()


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
    y=(time.strftime("%Y"))
    m=(time.strftime("%m"))
    month=(time.strftime("%B"))
    value=("wsprspots-" + y + "-" + m + ".csv." + ext)
       
    # get remote file size
    checkurl=(Url + value)
    req = requests.head(checkurl)
    req.content
    remote_size=(req.headers['content-length'])
    
    print("\n" + 45 * '-')
    print(" Updating %s" % value)
    print(45 * '-')

    # download a new archive file if Local and Remote sizes do not match
    checkfile=(srcd + (os.sep) + value)
    if os.path.isfile(checkfile):
        try:
            local_size=(os.path.getsize(srcd + (os.sep) + value))
        except:
            local_size = 0
    else:
        local_size = 0

    if not (int(remote_size)) == (int(local_size)):
        download_files(value)
    else:
        clear_screen
        r = int(remote_size)
        l = int(local_size)
        print("* File Name ..........: %s" % value)
        print("* Remote File Size ...: {:,} bytes".format(r))
        print("* Local File Size ....: {:,} bytes".format(l))
        print("* Local File Status ..: Up to Date\n")

    # cleanup csvd directory
    clean_csvd()

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
    print(" Updating Tables - ( please be patient )")
    print(45 * '-')
    ttime1 = time.time()
    total_records=0
    total_size=0

    # create the update list
    for fname in os.listdir(srcd):
        if fname.endswith(ext):
            ulist.append(fname)

    # loop through each file, get stats, update the database status table
    for value in sorted(ulist):
        extract_file(value)
        fname = (value)
        utime = time.strftime("%Y-%b-%d",time.gmtime())
        lines = (records)
        columns = (csv_cols)
        update_stats(value,utime,columns,lines)
        trecords += records
        tfsize += fsize
        tfcount += 1

    ttime2 = ((time.time()-ttime1)/60)

    # print the summary
    print("\n" + 45 * '-')
    print(" Status Table Update Summary")
    print(45 * '-')
    print(" * Total Files .......: {:,}".format(tfcount))
    print(" * Total Records .....: {:,}".format(trecords))
    print(" * Total Bytes .......: {:,}".format(tfsize))
    print(" * Processing Time ...: %.1f minutes \n" % ttime2)

    # now clean csvd directory
    clean_csvd()


#---------------------------------------------- Create csv file from all tar.gz
def search_all_months_for_callsign():
    """Search All Archive Files For A Given Callsign
    
    Original Script by ...: Gian Piero I2GPG
    Modified by ..........: Greg Beam, KI7MT
    
    Actions Performed:
        1. Searches ALL downloaded archive files for a given callsign
        2. Creates a .csv file: <call>-<month>-<year>.csv

    """
    # reset timers and prompt user for callsign
    reset_timers()
    call = raw_input("Enter callsign to log: ")
    call = call.upper()
    
    # create the output file name and open the filw for writing
    mylogfile = reports + (os.sep) + call + "-all" + ".csv"
    w = open(mylogfile, "w")
    
    # get the list and count of all archive files
    months = sorted(glob.glob(srcd + (os.sep) + '*.gz'), key=os.path.basename)
    nmonths = len(months)
    print("\n" + 45 * '-')
    print(" Searching %s Archive Files for [ %s ]" % (str(nmonths),call))
    print(45 * '-')

    # loop through each file and extract lines containing <callsign>
    qt1 = time.time()
    for count in range (nmonths):
        file_name = months[count].split("wsprspots-",1)[1]
        print("* Processing ..: wsprspots-%s " % file_name)
        r=gzip.open(months[count], "r")
        for line in r:
            if call in line:
                x=line.split(',')                                   # split data fields
                if (x[2] == call) or (x[6] == call):                # callsign or reporter fields only
                    s = float(x[1])                                 # decode and replace time stamp
                    d = time.strftime('%Y-%m-%d', time.gmtime(s))
                    t = time.strftime('%H%M', time.gmtime(s))
                    timestamp = str(d) + ',' + str(t)
                    newl = x[0] + ',' + timestamp
                    for count in range (len(x)-2):                  # copy rest of the line
                        newl = newl + ',' + x[count + 2]
                    w.write(newl,)                                  # write line to output file
    r.close()          
    w.close()
    qt2 = ((time.time()-qt1)/60)
    print("--End of Job--")
        
    # get total number of entries in <call>-all.csv file
    with open(mylogfile,"r") as f:
        reader = csv.reader(f,delimiter = ",")
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

    # cleanup csvd directory
    clean_csvd()


#-------------------------------------------- Search current month for callsign
def search_current_monnth_for_callsign():
    """Search Current Month For A Given Callsign
        
    Original Script by ...: Gian Piero I2GPG
    Modified by ..........: Greg Beam, KI7MT

    Actions Performed:
        1. Updates the current months archive file
        2. Creates a .csv file: <call>-<month>-<year>.csv

    """
  
    # reset timers and update current monthly archive file
    reset_timers()
    update_current_month()
 
    # get data parameters
    now =  today.strftime("%B-%Y")
    y = (time.strftime("%Y"))
    m = (time.strftime("%m"))
    count = 0

    # create the file name to search
    value = ("wsprspots-" + y + "-" + m + ".csv." + ext)
    
    # prompt the user for callsign input
    call = raw_input("Enter callsign to check: ")
    call=call.upper()

    # setup the output file name
    mylogfile = reports + (os.sep) + call + '-' + time.strftime("%B") + '-' + y + ".csv"

    # open the log file and set the file name to check
    w = open(mylogfile, "w")
    month = (srcd + (os.sep) + (os.sep) + value)
    name = (value)
    print("\n" + 45 * '-')
    print(" Processing [ %s ] for %s" % (call,now))
    print(45 * '-')

    # start the timer and open the archive file    
    qt1 = time.time()
    r=gzip.open(month, "r")
    
    # start the main loop
    for line in r:
        if call in line:
            x = line.split(",")                         # split data fields
            if (x[2] == call) or (x[6] == call):        # callsign or reporter fields only
                s = float(x[1])                                # decode and replace time stamp
                d = time.strftime('%Y-%m-%d', time.gmtime(s))
                t = time.strftime('%H%M', time.gmtime(s))
                timestamp = str(d) + ',' + str(t)
                newl = x[0] + ',' + timestamp
                for count in range (len(x)-2):      #copy rest of the line
                    newl = newl + ',' + x[count + 2]
                w.write(newl,)                      # write line to output file

    r.close()          
    w.close()


    # get total number of entries in the new .csv file
    with open(mylogfile,"r") as f:
        reader = csv.reader(f,delimiter = ",")
        data = list(reader)
        ncount = len(data)
    
    f.close()
    
    # print the summary
    qt2 = ((time.time()-qt1)/60)
    print("* Process Time ...: %.1f minutes" % qt2)
    print("* Log Count ......: %s " % ncount)
    print("* File Location ..: %s " % mylogfile)

    # cleanup csvd directory
    clean_csvd()


#---------------------------------------------------------- Main Menu Functions
def main():
    """Main Menu Functions
    
    Function Notes:
        1. Creates required directories
        2. Sets the archive file extension based on the platform
        3. After each action the csvd directory is cleaned
        4. The pause statement sets up return to main menu
        
        NOTE: Entries must match the items in print_menu() function.
    
    """
    create_dirs()
    set_ext()
    clear_screen()
    while True:
        print_menu()
        selection = raw_input("Your selection: ")
        if "1" == selection:
            check_archive()
            pause()
            main()

        if "2" == selection:
            update_status_table()
            pause()
            main()

        if "3" == selection:
            update_current_month()
            pause()
            main()

        if "4" == selection:
            search_all_months_for_callsign()
            pause()
            main()

        if "5" == selection:
            search_current_monnth_for_callsign()
            pause()
            main()

        if "6" == selection:
            afiles = len(glob.glob1(csvd,"*.csv"))
            print("\n" + 45 * '-')
            print(" Cleanup CSV Directory")
            print(45 * '-')
            if afiles == 0:
                print(" * CSV Directory Is Clean, Nothing To Be Done \n")
            else:
                print(" * Removing [ %s ] files from CSV Directory" % nfiles)
                clean_csvd()
                print(" * Finished Cleanup")
            
            pause()
            main()
            
        if "7" == selection:
            return

        else:
            return


#-------------------------------------------------------------------- Main Menu
def print_menu():
    """Prints The Main Menu

    Actions Performed:
        1. Synchronize WSPRnet Archive Files
        2. Update Database Status Table
        3. Update [ %s ] Archive File
        4. Callsign Search Of All Archive Files
        5. Callsign Search For <Current Month>
        6. Clean Up CSV Directory
    
        Note: Synchronizing and Updating the the Status Table can take
              several minutes depending on Internet speeds and your
              systems computer processor / disk speeds. It is not uncommon
              for each process between 20-30 minutes. 
        
    """
    cmon =  today.strftime("%B")
    print(45 * "-")
    print(" WSPR Database Main Menu")
    print(45 * "-")
    print(" 1. Synchronize WSPRnet Archive Files")
    print(" 2. Update Database Status Table")
    print(" 3. Update [ %s ] Archive File" % cmon)
    print(" 4. Callsign Search Of All Archive Files")
    print(" 5. Callsign Search For [ %s ] " % cmon)
    print(" 6. Clean Up CSV Directory")
    print(" 7. Exit")
    print("")

       
if __name__ == "__main__":
    main()

# END WsprDB
