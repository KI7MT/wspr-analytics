Overview
--------
Wspr-Ana provides a set of common functions to download and parse
database archive files from `WSPRnet`_.

The download lists are generated directly from `WSPRnet`_ archive URL. As
new files are added, they should be automatically picked up by and added
to the process list. This includes the the current month which is updated
in early hours UTC each day.

The script should work with either Python2 or Python3. It will also auto
select the extension based on running Windows ``.zip`` or Linux ``.gz``


Requirements
------------
``Python2.5+`` or ``Python3.0+`` interrupter in your ``$PATH / %PATH%``


Python Modules
--------------

The following assumes a base install with no additional modules added. For
Linux, you may also satisfy the requirements with your package manager
if they are available.

.. code-block:: python

   pip install beautifulsoup4
   pip install clint
   pip install requests


For Debian / Ubuntu based distributions, you can install the required
packages with:

.. code-block:: bash

   Python2
   sudo apt-get install python-bs4 python-clint python-requests

   Python3
   sudo apt-get install python3-bs4 python3-clint python3-requests


Installation and Usage
----------------------
If you have already downloaded all the archive files from `Download Section`_ on
`WSPRnet`_, copy them to the srcd directory after cloning.

1. git clone git://git.code.sf.net/u/ki7mt/wspr-ana
2. Copy previously downloaded WSPRNet archive files to ./wspr-ana/srcd
3. To run, type: ./wsprana.py
4. For the first run, select Option-1 to sync archive files
5. After initial database sync, you can search all or the current
   month for a given callsign.


Variables and Scripts
---------------------

For the users convenience, a preloaded database has already been provided.
This help prevent anomalies with downloads an initial status table updates.

**The folder and file structures are as follows**

- ``srcd``, Directory for WSPRNet archive files
- ``csvd``, Directory for extracted csv files
- ``reports``, Directory for output files
- ``wsprana.db``, SQLite3 Database
- ``wsprana.sql``, SQL template for pre-loading the database
- ``wsprana.py``, Main script


Default Database
----------------

A default database, updated as of the latest git posting, is provided in
the repository. The data contained in the ``[ status ]`` table contains the
following fields:

- ``name``, archive file name from WSPRNet
- ``date``, the date the status was last updated
- ``column``,  the number of columns for the archive file
- ``records``, the number of records in the archive .csv file


.. _WSPRnet: http://wsprnet.org/drupal/
.. _Download Section: http://wsprnet.org/drupal/downloads
