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

* Download / Update all `WSPRnet`_ archive files
* Download / Update current month archive file
* Generate call sign specific raw CSV files
* Generate call sign specific `Epoch`_ converted ( human readable ) CSV files
* Generate ``Spots per Band per Day`` for current month

Much more is planned for as time allows... stay tunned!

.. note::

    During development, this package **is not** intended for pip installaiton.
    It should be checked out and run from source.

.. _WSPRnet: http://wsprnet.org/drupal/
.. _Download Section: http://wsprnet.org/drupal/downloads
.. _Epoch: https://en.wikipedia.org/wiki/Unix_time
