#! /usr/bin/env python

import zipfile
import sys
import os

args = sys.argv
filepath = args[1]

with zipfile.ZipFile(args[1] + '.zip','w',zipfile.ZIP_DEFLATED) as zf:
    zf.write(args[1])
