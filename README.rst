Overview
--------
WSPR Analysis provides a set of functions to download and parse database
archive files from `WSPRnet`_ to enable post even analysis.

The download lists are generated directly from `WSPRnet`_ archive URL. As
new files are added, they should be picked up by and added to the process list.
This includes the the current month which is updated in early hours UTC each
day.

At present, the scripts only work with Python3, however, they will auto
select the extension based on running Windows ``.zip`` or Linux ``.gz``

At the time of this writing the following features are enabled:

* Automated downloads of all or current month archive files
* Generate call-sign specific CSV files for off line analysis
* Generate ``Spots per Band per Day`` for current month

Much more is planned for as time allows... stay tunned!

.. _WSPRnet: http://wsprnet.org/drupal/
.. _Download Section: http://wsprnet.org/drupal/downloads

