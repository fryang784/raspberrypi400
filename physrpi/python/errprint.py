#!/usr/bin/env python3

#
# errprint.py - Print error message to stdout
#
# 04May17  Everett Lipman
#

import sys

print()

print('This message has been sent to stdout.')

print()

print('This is an error message, sent to stderr.', file=sys.stderr)

print()
