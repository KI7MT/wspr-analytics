# Installation

At the time of this writing, usage has only been tested on Linux x86-64 and.
There is no particular reason why installation and usage could not be done on
Windows or Mac OSX if the Requirements are met.

It is `Highly Recommended` to use [Anaconda][] from Continuum Analytics`. 
It's free, supports all major operating systems, is well supported, does not
interfere with system level packaging, can be installed on a per user basics
and provides everything needed for **Comprehensive WSPR Data Analysis**.

## Installing Anaconda

Installing [Anaconda][] is very easy. Simply download the shell script and
run it in a terminal:

.. code-block:: bash

   bash Anaconda3-4.0.0-Linux-x86_64.sh

Follow the prompts and when asked, I elected to add the the source scripts to
my `.bashrc` but that is entirely up to you. I also used the default
installation direcotry of:

```bash
/home/$USER/anaconda3
```


## Upgrade Anaconda

This is part of [30 Minute Conda][] getting started page, but for completeness,
I'm adding what was needed for my environment. All actions are performed in a
terminal, open as required on your system, then:

First,  [Anaconda][] should be upgraded:

```bash
conda update conda
```

Next, update the conda-env scripts:

```bash
conda update conda-env
```

That is all for the basic [Anaconda][] installation and update. You should
close, then re-open your terminal to ensure all the paths and updates are
working proerpy.


## Additional Python Modules

One package that is not available is a [conda][] package is [AppDirs][] but can
be installed with [Pip][]. In the terinal:

```bash
pip install appdirs clint
```

## Installing R

The [R-Scripting][] language in not part of the base [Anaconda][] installation,
however, installation is fairly easy using [conda][], the [Anaconda][] package
manager.

Again, in the terminal, perform the following:

```bash
conda install -c r r-essentials
conda install -c r r-gridextra
```

[Anaconda]: https://www.continuum.io/downloads
[Continuum Analytics]: https://www.continuum.io/
[30 Minute Conda]: http://conda.pydata.org/docs/test-drive.html
[R-Scripting]: https://www.r-project.org/about.html
[conda]:  http://conda.pydata.org/docs/using/pkgs.html
[Pip]: https://pypi.python.org/pypi/pip
[AppDirs]: https://pypi.python.org/pypi/appdirs
