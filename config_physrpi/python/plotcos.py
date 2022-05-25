#!/usr/bin/env python3

#
# plotcos.py - Plot cos(x)
#
# 13Jul16  Everett Lipman
#
USAGE="""
usage: plotcos.py N

       N is the number of complete periods to plot.
"""
NPOINTS = 512

import sys
import os

if len(sys.argv) != 2:
   print(USAGE, file=sys.stderr)
   print('', file=sys.stderr)
   exit(1)

try:
   N = float(sys.argv[1])
except ValueError:
   print('\nCannot convert "%s" to a number of periods.\n'
         % sys.argv[1], file=sys.stderr)
   print(USAGE, file=sys.stderr)
   print('', file=sys.stderr)
   exit(1)

import numpy as np
import matplotlib.pyplot as plt

xvals = np.linspace(0, 2.0*N*np.pi, NPOINTS)

f1, ax1 = plt.subplots()
ax1.plot(xvals,np.cos(xvals))
f1.show()

input("\nPress <Enter> to exit...\n")
