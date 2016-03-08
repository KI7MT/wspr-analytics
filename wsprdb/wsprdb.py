#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       wsprdb.py
#
#       Copyright 2016 Greg Beam <ki7mt@yahoo.com>
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
__version__ = '0.0.1'
__license__ = "GNU General Public License (GPL) Version 3"
__version_info__ = (0, 0, 1)
__author__ = 'Greg Beam'
__email__ = '<ki7mt@yahoo.com>'
__status__ = 'Development'

"""
**WsprDB:**  Provides a set of commonly used tools to download and parse
database archive files from Wsprnet.org.

Performs the following functions:
    - abc
    - abc
    - abd
"""

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
import appdirs
from clint.textui import progress
from bs4 import BeautifulSoup

usage = """python wsprdb.py <module-name>"""

def setup_common_dirs():
    """Create directories and variables

    Sets database directory based on standard File System Hierarchy
    - Linux ....: $HOME/.local/share/ + <dir-name>
    - Windows ..: C:\Users\%username%\AppData\local\ + <dir-name>

    srcd .......: Source Directory for WSPRnet.org archive files
    cvsd .......: Directory for holding extracted csv files
    dbname .....: Name of the SQLite3 database

    """
    shared = appdirs.AppDirs("WSPR-LOG", appauthor='', version='', multipath='')
    shared = shared.user_data_dir
    srcd = ('/media/ki7mt/data/wsprdb')
    csvd = (shared + (os.sep) + "csvd")
    Url="http://wsprnet.org/archive/"
    dbname = 'wsprana.db'
    dbf = (shared + (os.sep) + dbname)
    dirs=(shared, srcd, csvd)

    for i in dirs():
        if not os.path.exists(i):
            os.mkdir(i)
        
    return shared, srcd, csvd, Url, dbname, dbf


def archive_ext()
    """Set archive file extension ( zip or gz ) based on operating
    system type
    """
    if sys.platform == "win32":
        ext = "zip"
    else:
        ext = "gz"
    
    return ext

def reset_timers():
    """Reset values before running queries"""
    qt1 = 0
    qt2 = 0
    qt3 = 0
    qt4 = 0
    qt5 = 0
    qt6 = 0

def clear_screen():
    """Clear based on the platform"""
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')

def init_db():
    """Create database structure and add default table data"""
    qt1 = time.time()
    print( 50 * '-')
    print("Creating New WSPR Analysis Database")
    print( 50 * '-')

    # connect to SQLite3 database
    with sqlite3.connect(dbf) as conn:
        cur = conn.cursor()

        # get the Sqlite3 version
        cur.execute("""SELECT SQLITE_VERSION()""")
        sv = cur.fetchone()

        # drop tables if they exist
        cur.execute('''DROP TABLE IF EXISTS appdata''')
        cur.execute('''DROP TABLE IF EXISTS records''')
        cur.execute('''DROP TABLE IF EXISTS status''')
        conn.commit()

        # create appdata table
        cur.execute("""CREATE TABLE appdata(
            author      TEXT,
            copyright   TEXT,
            license     TEXT,
            version     TEXT,
            email       TEXT,
            status      TEXT
        );""")
        
        # default values
        author = (__author__)
        copyright = (__copyright__)
        license = (__license__)
        version = (__version__)
        email = (__email_)
        status = (status__)
        cur.execute("""NSERT INTO appdata(author,copyright,license,version,
                    email,status) VALUES (?,?,?,?,?,?);""", (author,copyright,
                    license,version,email,status))
        
        # create archive status table
        cur.execute("""CREATE TABLE IF NOT EXISTS status(
                    name           TEXT    PRIMARY KEY UNIQUE  NOT NULL,
                    date_added     TEXT,
                    columns        TEXT,
                    records        TEXT
        );""")
 
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

#------------------------------------------------------- database version
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

#------------------------------------------------------- database version
def version_db():
    """Get the wsperdb version"""
    with sqlite3.connect(dbf) as conn:
        cur = conn.cursor()    
        cur.execute('SELECT * FROM appdata ORDER BY ROWID ASC LIMIT 1')
        for row in cur.fetchall():
            dbv = row[3]
    
    conn.close()
    return dbv

#------------------------------------------------------- md5sum the gz file
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

#------------------------------------------------------- add csv file to db
def add_csv_file(value):
    """
    Add an archive file from WSPRnet.org/achieves
    MD5SUM check file
    Unpack the file ( zip or gz )
    
    Count the columns in the CSV file. Versions prior to 2010 have 13 fields
    Update the status table
    """
    print("* Database .......: {}".format(dbname))
    csvfile = (shared + (os.sep) + value)
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

#------------------------------------------------------- parse html page
def csvf(Url):
    """
    Parse wsprnet.org/archive html page and extract file names
    """
    list = BeautifulSoup(requests.get(Url).text, "html.parser")
    for a in list.find_all('a'):
        yield a['href']

#------------------------------------------------------- DownloaFiles
def download_files(value):
    """
    Download wsprspot archive files
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
    # Note: this can take a long time >=25-30 minutes the first run
    extract_file(value)
    fname = (value)
    utime = time.strftime("%Y-%b-%d",time.gmtime())
    lines = (records)
    columns = (csv_cols)
    update_stats(value,utime,columns,lines)


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
    os.chdir(shared)
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

#------------------------------------------------------- check the db archive
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
                print("* {} with {:,} bytes is Up To Date".format(l,local_size))
                
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
    print(45 * '-')
    print(" Archive Summary")
    print(45 * '-')
    print("* Total Archives ..: %s " % lcount)
    print("* Updates Needed ..: %s \n" % ix)
    if ix > 0:
        for value in sorted(dwn_list):
            download_files(value)

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
    
    clear_screen()
    print(45 * '-')
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
        clear_screen()
        print(45 * '-')
        print(" Updating Archive for %s %s" % (month,y))
        print(45 * '-')
        download_files(value)
    else:
        clear_screen
        r = int(remote_size)
        l = int(local_size)
        print("* File Name ..........: %s" % value)
        print("* Remote File Size ...: {:,} bytes".format(r))
        print("* Local File Sise ....: {:,} bytes".format(l))
        print("* Local File Status ..: Up to Date\n")

#------------------------------------------------------- unpack archive
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

if __name__ == '__main__':
    globals()[sys.argv[1]]()

# END WsprDB
