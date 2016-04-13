#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
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

#
#       wsprdb.py
#
#       Copyright 2016 Greg Beam <ki7mt@yahoo.com>
#       Copyright 2016 Gian Piero I2GPG <i2gpg@wedidit.it> 
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; Version 3 of the License
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, the license can be downloaded here:
#
#       http://www.gnu.org/licenses/gpl.html

# Meta
__author__ = 'Greg Beam, Gian Piero' 
__copyright__ = 'GPLv3'
__version__ = '1.0.0'
__version_info__ = (1, 0, 0)
__email__ = '<ki7mt@yahoo.com>, <i2gpg@wedidit.it>'
__status__ = 'Development'
__license__ = "GNU General Public License (GPL) Version 3"
"""
 REQUIREMENTS
 * Python2 or Python3 interrupter in your $PATH / %PATH%
 

 PYTHON MODULES
 The following assumes a base install with no additional modules added. For
 Linux, you may also satisfy the requirements with your package manager
 if they are available.
 
 * pip install beautifulsoup4
 * pip install clint
 * pip install requests
 

 INSTALLATION and USAGE
 
 Using the Git Repository:
 1. git clone git://git.code.sf.net/u/ki7mt/wsprdb
 2. Copy previously downloaded WSPRNet archive files to ./wsprdb/srcd
 
 To run, type: ./wsprdb.py
 

 OVERVIEW
 
 WsprDB provides a set of commonly used functions to download and parse
 database archive files from Wsprnet.org.

 The download lists are generated directly from WSPRnet.org archive URL. As
 new files are added, they should be automatically picked up by **WsprDB**
 and added to the process list. This includes the the current month which
 is updated in the early hours UTC each day.
 
 The script should work with either Python2 or Python3. It will also auto
 select the extension based on running Windows (.zip) or Linux (.gz)

 The following Functions Are Currently Employed:
 * Creates and SQLite3 database for housing data ( default db is provided )
 * Download all archive files from Wsprnet.org
 * Size check local and remote archives, download if they do not match
 * Creates a monthly .csv fle for a given callsign
 * Creates a .csv file from all WSPRNet archives for a given callsign

 Directory Structure and Variables:
 * srcd .....: User defined source directory for WSPRnet.org archive files
 * csvd .....: Directory for holding extracted csv files
 * reports ..: Directory for output files
 * dbname ...: Name of the SQLite3 database
 * sqlf .....: SQL template for loading the SQLit3 database if needed
 
 If you have previously downloaded the archive files, copy thenm to the
 folder named srcd.
 
 A default database, updated as of the latest git posting, is provided in
 the repository. The data contained in the [ status ] table contains the
 following fields:
 
 name ......: archive file name from WSPRNet
 date ......: the date the status was last updated
 column ....: the number of columns for the archive file
 records ...: the number of records in the archive .csv file
"""
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


#----------------------------------------------------------- set file extension
"""Set archive file extension ( zip or gz ) based on operating system type"""
if sys.platform == "win32":
    ext = "zip"
else:
    ext = "gz"


#----------------------------------------------------------- set file extension
"""Create directories if they do not exist"""
for z in dirs:
    d=(appdir + (os.sep) + z)
    if not os.path.exists(d):
        os.mkdir(d)


#----------------------------------------------------------------- reset timers
def reset_timers():
    """Reset values before running queries"""
    qt1 = 0
    qt2 = 0
    qt3 = 0
    qt4 = 0
    qt5 = 0
    qt6 = 0


#----------------------------------------------------------------- Clean Screen
def clear_screen():
    """Clear based on the platform"""
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')


#---------------------------------------------------------- Initialize Database
def init_db():
    """Create database structure and add default table data"""
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


#------------------------------------------------------------- database version
def check_db():
    """
    Check if we can connect to the database, if not, init_db
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


#------------------------------------------------------------- database version
def version_db():
    """Get the wsperdb version"""
    with sqlite3.connect(dbf) as conn:
        cur = conn.cursor()    
        cur.execute('SELECT * FROM appdata ORDER BY ROWID ASC LIMIT 1')
        for row in cur.fetchall():
            dbv = row[3]
    
    conn.close()
    return dbv


#----------------------------------------------------------- md5sum the gz file
def md5(fname):
    """
    Simple MD5SUM function for checking files.
    Source: http://stackoverflow.com/questions/3431825/    
    """
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    f.close()
    return hash_md5.hexdigest()


#----------------------------------------------------------- add csv file to db
def add_csv_file(value):
    """
    Add an archive file from WSPRnet.org/achieves
    MD5SUM check file
    Unpack the file ( zip or gz )
    
    Count the columns in the CSV file. Versions prior to 2010 have 13 fields
    Update the status table
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

    # now cleanup the csv direcroty
    clean_csvd()


#--------------------------------------------- remove all .csv files from csvd
def clean_csvd():
    os.chdir(csvd)
    file_list = glob.glob("*.csv")
    for f in file_list:
        os.remove(f)
    
    os.chdir(appdir)


#-------------------------------------------------------------- parse html page
def csvf(Url):
    """
    Parse wsprnet.org/archive html page and extract file names
    """
    list = BeautifulSoup(requests.get(Url).text, "html.parser")
    for a in list.find_all('a'):
        yield a['href']


#--------------------------------------------------------------- Download Files
def download_files(value):
    """
    Download wsprspot archive files
    Note: this can take a long time >= 25-30 minutes the first run
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


#------------------------------------------------- Update database status table
def update_stats(value,utime,columns,lines):
    """
    Update the database stats table for each archive files
    """
    conn = sqlite3.connect(dbf)
    cur = conn.cursor()
    cur.execute('''REPLACE into status(name,date_added,columns,records)
                values (?,?,?,?);''', (value,utime,columns,lines))
    conn.commit()
    conn.close()

#--------------------------------------------------------- Extract archive file
def extract_file(value):
    """
    Extract downloaded archive files
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
            print("* File is empty ..: {}".format(dest_name))

    # Now clean upd csvd directory
    clean_csvd()

#--------------------------------------------------------- check the db archive
def check_archive():
    """
    Check each archive file for changes
    """
    print(65 * '-')
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
                
    # check if archive data is missing from status table
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


#---------------------------------------------------- update current month only
def update_current_month():
    """
    Update current month archive file.
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

    # get local file size
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


#--------------------------------------------------------------- unpack archive
def update_status_table():
    ulist = []
    print(45 * '-')
    print(" Updating Tables - ( please be patient )")
    print(45 * '-')
    ttime1 = time.time()
    total_records=0
    total_size=0

    for fname in os.listdir(srcd):
        if fname.endswith(ext):
            ulist.append(fname)

    for value in sorted(ulist):
        extract_file(value)
        fname = (value)
        utime = time.strftime("%Y-%b-%d",time.gmtime())
        lines = (records)
        columns = (csv_cols)
        update_stats(value,utime,columns,lines)
        
    ttime2 = (time.time()-ttime1)
    print(" Total Processing Time In sec ..: %.3f" % ttime2)

    # now clean csvd directory
    clean_csvd()


#---------------------------------------------- create csv file from all tar.gz
def search_all_months_for_callsign():
    """
    Credit Original Script ...: Gian Piero I2GPG
    Modified by ..............: Greg Beam, KI7MT 
    
    1. Creates wsprlog-<call>-all.csv file based on all WSPRnet archive files
    """
    reset_timers()
    call = raw_input("Enter callsign to log: ")
    call = call.upper()
    mylogfile = reports + (os.sep) + call + "-all" + ".csv"

    w = open(mylogfile, "w")
    months = sorted(glob.glob(srcd + (os.sep) + '*.gz'), key=os.path.basename)
    nmonths = len(months)
    print("\n" + 45 * '-')
    print(" Searching %s Archive Files for [ %s ]" % (str(nmonths),call))
    print(45 * '-')

    qt1 = time.time()
    for count in range (nmonths):
        file_name = months[count].split("wsprspots-",1)[1]
        print("* Processing ..: wsprspots-%s " % file_name)
        r=gzip.open(months[count], "r")
        for line in r:
            if call in line:
                x=line.split(',')                       # split data fields
                if (x[2] == call) or (x[6] == call):    # callsign or reporter fields only
                    t = gmtime(float(x[1]))             # decode and replace time stamp
                    timestamp = str(t[0])+'-'+str(t[1])+'-'+str(t[2])+','+str(t[3])+':'+str(t[4])
                    newl = x[0]+','+timestamp
                    for count in range (len(x)-2):      #copy rest of the line
                        newl = newl+','+x[count+2]
                    w.write(newl,)                      # write line to output file
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
    
    # priont job summary data
    print("\n" + 45 * '-')
    print(" Search Summary For [ %s ]" % call)
    print(45 * '-')
    print("* Files Processed ..: %s " % nmonths)
    print("* Log Entry Count ..: %s " % ncount)
    print("* Process Time .....: %.1f minutes" % qt2)
    print("* File Location ....: %s " % mylogfile)
    print ("\n")


#------------------------------------ update csv file from current month tar.gz
def search_current_monnth_for_callsign():
    """
    Credit Original Script ...: Gian Piero I2GPG
    Modified by ..............: Greg Beam, KI7MT 

    This function performs two actions:
     1. Updates the current month WSPRnet ( *.zip / .gz )  file
     2. Creates a .csv file: <call>-<month>-<year>.csv
    """
  
    # update the current month tar.gz
    reset_timers()
    update_current_month()
 
    # get data parameters
    now =  today.strftime("%B-%Y")
    y = (time.strftime("%Y"))
    m = (time.strftime("%m"))
    count = 0

    value = ("wsprspots-" + y + "-" + m + ".csv." + ext)
    call = raw_input("Enter callsign to check: ")
    call=call.upper()
    mylogfile = reports + (os.sep) + call + '-' + time.strftime("%B") + '-' + y + ".csv"
    w = open(mylogfile, "w")

    month = (srcd + (os.sep) + (os.sep) + value)
    name = (value)
    print("\n" + 45 * '-')
    print(" Processing [ %s ] for %s" % (call,now))
    print(45 * '-')

    qt1 = time.time()
    r=gzip.open(month, "r")
    for line in r:
        if call in line:
            x=line.split(',')                   # split data fields
            if (x[2]==call) or (x[6]==call):    # callsign or reporter fields only
                t=gmtime(float(x[1]))           # decode and replace time stamp
                timestamp=str(t[0])+'-'+str(t[1])+'-'+str(t[2])+','+str(t[3])+':'+str(t[4])
                newl=x[0]+','+timestamp
                for count in range (len(x)-2):  #copy rest of the line
                    newl = newl+','+x[count+2]
                w.write(newl,)                  # write line to output file

    r.close()          
    w.close()

    # get total number of entries in the new .csv file
    with open(mylogfile,"r") as f:
        reader = csv.reader(f,delimiter = ",")
        data = list(reader)
        ncount = len(data)
    
    f.close()
    qt2 = ((time.time()-qt1)/60)
    print("* Process Time ...: %.1f minutes" % qt2)
    print("* Log Count ......: %s " % ncount)
    print("* File Location ..: %s " % mylogfile)
    print ("\n")


#-------------------------------------------------------------------- main menu
def print_menu():
    cmon =  today.strftime("%B")
    print(45 * "-")
    print(" WSPR Database Main Menu")
    print(45 * "-")
    print(" 1. Syncronize All WSPRnet Archive Files")
    print(" 2. Update Database Tables")
    print(" 3. Update [ %s ] Archive File" % cmon)
    print(" 4. Callsign Search Of All Archive Files")
    print(" 5. Callsign Search For [ %s ] " % cmon)
    print(" 6. Clean Up CSV Directory")
    print(" 7. Exit/Quit")
    print("")


#---------------------------------------------------------------- main function
def main():
    clear_screen()
    while True:
        print_menu()
        selection = raw_input("Your selection: ")
        if "1" == selection:
            check_archive()

        if "2" == selection:
            update_status_table()

        if "3" == selection:
            update_current_month()

        if "4" == selection:
            search_all_months_for_callsign()

        if "5" == selection:
            search_current_monnth_for_callsign()

        if "6" == selection:
            clean_csvd()

        if "7" == selection:
            return

        else:
            return
        
if __name__ == "__main__":
    main()

# END WsprDB
