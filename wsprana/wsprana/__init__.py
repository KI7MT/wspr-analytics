#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from os import name, path
from os.path import expanduser

__version__ = "0.1.0"
__title__ = 'wsprana'
__author__ = 'Greg Beam, KI7MT'
__license__ = 'Apache License, Version 2.0'
__email__ = 'ki7mt@yahoo.com'

__home_dir__ = expanduser("~")
"""User home directory for Linux: /home/$USER"""

if os.name == 'nt':
    __wsprana_share__ = os.path.join(os.getenv(['LOCALAPPDATA']),__title__)
else:
    __wsprana_share__ = os.path.join(H__home_dir__,'.local','share',__title__)
r"""
    User share directory
        Linux: /home/$USER/share
        MacOS: /Users/$USER/share
        Win32: C:\Users\%USERNAME%\AppData\local\wsprana
"""

if os.name == 'nt':
    __wsprana_config__ = __wsprana_share__
else:
    __wsprana_config__ = os.path.join(H__home_dir__,'.config',__title__)
r"""
    User share directory: /home/$USER/.config/wsprana
        Linux: /home/$USER/share/wsprana
        MacOS: /Users/$USER/share/wsprana
        Win32: C:\Users\%USERNAME%\AppData\local\wsprana
"""

__csvd__ = os.path.join(__wsprana_share__,__title__,'csvd')
r"""
    CSV share for downloaded WSPRnet csv files
        Linux: /home/$USER/.local/share/wsprana/csvd
        MacOS: /Users/$USER/.local/share/wsprana/csvd
        Win32: C:\Users\%USERNAME%\AppData\local\wsprana\csvd
"""

__parquetd__ = os.path.join(__wsprana_share__,__title__,'parquet')
r"""
    Parquest share for converted parquet files
        Linux: /home/$USER/.local/share/wsprana/parquet
        MacOS: /Users/$USER/.local/share/wsprana/parquet
        Win32: C:\Users\%USERNAME%\AppData\local\wsprana\parquet
"""