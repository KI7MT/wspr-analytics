# -*- coding: utf-8 -*-
# Copyright 2020 Greg Beam, KI7MT
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import setuptools

import wsprana

here = os.path.dirname(os.path.abspath(__file__))

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=wsprana.__title__,
    version=wsprana.__version__,
    author=wsprana.__author__,
    license=wsprana.__license__,
    author_email=wsprana.__email__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    python_requires='>=3.6.*',
    project_urls={
        'WSPR Analytics Source': 'https://github.com/KI7MT/wsprana',
    },
    packages=setuptools.find_packages(),
    install_requires=[
        'pyspark',
        'beautifulsoup4',
        'requests',
        'appdirs',
        'clint',
    ],
    package_data={
        'wsprana': [
            'wsprana/resources/wsprana.sql',
        ]
    },
    entry_points={
        'console_scripts': ['wsprana = wsprana.wsprana:main'],
    },
    zip_safe=False,
    classifiers=[
        "Natural Language :: English",
        "Development Status :: 1 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Utilities",
        "Topic :: Database",
        "Topic :: Communications :: Ham Radio",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    url='https://github.com/KI7MT/wsprana',
)
