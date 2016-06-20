#!/usr/bin/env python

from distutils.core import setup

setup(
    name='wspr-ana',
    version=open("wsprana/_version.py").readlines()[-1].split()[-1].strip("\"'"),
    description='WSPR Data Analysis Tools',
    author='Greg Beam',
    author_email='ki7mt@yahoo.com',
    url='https://github.com/KI7MT/wspr-ana',
    packages=['wspr-ana'],
    keywords='WSPR sqlite pandas dataframe ',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Topic :: Communications :: Ham Radio",
        "Topic :: Utilities",
    ],
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'beautifulsoup4',
        'requests'
    ]
)
