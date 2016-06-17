Installation
------------

At the time of this writting, usage has only been tested on Linux. There is
no particular reason installation and usage could be done on Windows or
Mac OSX if the `Requirements`_ are met. 


.. _Requirements:

Requirements
------------
* Python2.7.x or Python3.x
* R scripting language
* `Python Modules`_, beautifulsoup4, requests, clint


.. _Python MOdules:

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


General Usage
-------------
If you have already downloaded all the archive files from Download Section on
WSPRnet, copy them to the srcd directory after cloning.

1. git clone git://git.code.sf.net/u/ki7mt/wspr-ana
2. Copy previously downloaded WSPRNet archive files to ./wspr-ana/srcd
3. To run, type: ./wsprana.py
4. For the first run, select Option-1 to sync archive files
5. After initial database sync, you can search all or the current
   month for a given callsign.

