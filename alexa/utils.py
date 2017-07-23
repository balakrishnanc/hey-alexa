#!/usr/bin/env python
# -*- mode: python; coding: utf-8; fill-column: 80; -*-
#
# utils.py
# Created by Balakrishnan Chandrasekaran on 2017-07-23 17:33 +0200.
# Copyright (c) 2017 Balakrishnan Chandrasekaran <balakrishnan.c@gmail.com>.
#

"""
utils.py
Utility methods
"""

__author__  = 'Balakrishnan Chandrasekaran <balakrishnan.c@gmail.com>'
__version__ = '1.0'
__license__ = 'MIT'


import io
import requests


# Utility `file open` calls.
__open = lambda mode: lambda fname: io.open(fname, mode, encoding='utf-8')
fread  = __open('r')
fwrite = __open('w')
