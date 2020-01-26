#! /usr/bin/env python

import zipfile
import sys
import os

args = sys.argv
filepath = args[1]
basename = os.path.splitext(os.path.basename(filepath))[0]

with zipfile.ZipFile(args[1],'r') as zf:
    zf.extractall(basename)
