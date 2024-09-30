#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Copyright (C) 2015-2023 Daniel Rodriguez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
import os
import setuptools

# Package name
pname = 'backtrader'

# Directory of the package
here = os.path.abspath(os.path.dirname(__file__))

# Get the version from version.py
vname = 'version.py'
with open(os.path.join(here, pname, vname)) as f:
    exec(f.read())

setuptools.setup(
    name=pname,
    version=__version__,
    description='BackTesting Engine',
    long_description='A versatile backtesting framework for Python.',
    url='https://github.com/mementum/backtrader',
    author='Daniel Rodriguez',
    author_email='danjrod@gmail.com',
    license='GPLv3+',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Software Development',
        'Topic :: Office/Business :: Financial',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
    ],
    keywords=['trading', 'development'],
    packages=setuptools.find_packages(exclude=['docs', 'docs2', 'samples']),
    entry_points={'console_scripts': ['btrun=backtrader.btrun:btrun']},
    install_requires=[],
    extras_require={
        'plotting': ['matplotlib'],
    },
)
