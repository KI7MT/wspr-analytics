Installation
------------

At the time of this writting, usage has only been tested on Linux x86-64 and. There is
no particular reason why installation and usage could be done on Windows or
Mac OSX if the Requirements are met.

It is ``Highly Recommended`` to use `Anaconda`_ from `Continuum Analytics`_. 
It's free, supports all major operating systems, is well supported, does not
interfere with system level packaging, can be installed on a per user basics
and provides everything needed for **WSPR-Ana** and much more.

Installing Anaconda
^^^^^^^^^^^^^^^^^^^
Installing `Anaconda`_ is very easy. Simply download the shell script and
run it in a terninal:

.. code-block:: bash

   bash Anaconda3-4.0.0-Linux-x86_64.sh

Follow the prompts and when asked, I elected to add the the source scripts to
my ``.bashrc`` but that is entirely up to you. I also used the default
installation direcotry of:

.. code-block:: bash

   /home/<user-name>/anaconda3


Upgrade Anaconda
^^^^^^^^^^^^^^^^
This is part of `30 Minute Conda`_ getting started page, but for completeness,
I'm adding what was needed for my environment. All actions are perfomed in a
termainal, open as required on your system, then:

First,  `Anaconda`_ should be upgraded:

.. code-block:: bash

   conda update conda


Next, update the conda-env scripts:

.. code-block:: bash

   conda update conda-env

That is all for the basic `Anaconda`_ insatallaition and update. You should
close, then re-open your terminal to ensure all the paths and updates are
working proerpy.


Additional Python Modules
^^^^^^^^^^^^^^^^^^^^^^^^^^
One package that is not available is a `conda`_ package is `AppDirs`_ but can
be installed with `Pip`_. In the terinal:

.. code-block:: bash

   pip install appdirs


Installing R
^^^^^^^^^^^^
The `R-Scripting`_ language in not part of the base `Anaconda`_ installation,
however, installation is farily easy using `conda`_, the `Anaconda`_ package
manager.

Again, in the terminal, perform the following:

.. code-block:: bash

  conda install -c r r-essentials
  conda install -c r r-gridextra


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

.. _Anaconda: https://www.continuum.io/downloads
.. _Continuum Analytics: https://www.continuum.io/
.. _30 Minute Conda: http://conda.pydata.org/docs/test-drive.html
.. _R-Scripting: https://www.r-project.org/about.html
.. _conda:  http://conda.pydata.org/docs/using/pkgs.html
.. _Pip: https://pypi.python.org/pypi/pip
.. _AppDirs: https://pypi.python.org/pypi/appdirs
