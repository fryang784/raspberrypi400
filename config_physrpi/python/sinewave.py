#!/usr/bin/env python3

#
# sinewave.py - Store values of sin(x) in an array and plot them
#
# 16Feb16  Everett Lipman
#
NPOINTS = 40

USAGE="""
usage: sinewave.py [N]

       N is the number of points to compute in one period.
       Default is %d.
""" % NPOINTS

import sys
import os

nargs = len(sys.argv) - 1
if nargs > 1:
   print(USAGE, file=sys.stderr)
   print('', file=sys.stderr)
   exit(1)

if nargs == 1:
   try:
      N = int(sys.argv[1])
   except ValueError:
      print('\nCannot convert "%s" to a number of points.\n'
            % sys.argv[1], file=sys.stderr)
      print(USAGE, file=sys.stderr)
      print('', file=sys.stderr)
      exit(1)
else:
   N = NPOINTS

import numpy as np
import matplotlib.pyplot as plt

xvals = np.linspace(0, 2.0*np.pi, N)
sinvals = np.sin(xvals)

if N >= 10:
   nprint = 10
else:
   nprint = N

print()
for i in range(nprint):
   print('Value #%d: %.5f' % (i+1, sinvals[i]))
print()

f1, ax1 = plt.subplots()
ax1.plot(xvals, sinvals, '-', drawstyle='steps-post')
f1.show()

input("\nPress <Enter> to exit...\n")
