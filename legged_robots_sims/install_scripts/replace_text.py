#!/usr/bin/env python

import sys

# use: replace_text.py filepath searchtext replacetext outputfile

# Read in the file
with open(sys.argv[1], 'r') as file :
  filedata = file.read()

# Replace the target string
filedata = filedata.replace(sys.argv[2], sys.argv[3])

# Write the file out again
with open(sys.argv[4], 'w') as file:
  file.write(filedata)
