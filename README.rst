Overview
--------

Wspr-Ana provides a set of common functions to download and parse
database archive files from `WSPRnet`_.

The download lists are generated directly from `WSPRnet`_ archive URL. As
new files are added, they should be automatically picked up by and added
to the process list. This includes the the current month which is updated
in early hours UTC each day.

At present, the scripts only work with Python3, however, they will auto
select the extension based on running Windows ``.zip`` or Linux ``.gz``

At the time of this writing, there are only ``(2)`` plot reports that can
be generated,


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

