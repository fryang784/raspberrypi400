#!/usr/bin/env python3

#
# simple_plot.py - Plot x,y data with error bars
#
# 02May18  Adjusted plotting defaults
# 13Jul16  Everett Lipman
#
USAGE="""
usage: simple_plot.py datafile

       datafile is a 3-column text file containing numbers x,y,yerr.
       Data will be plotted with error bars of length 2*yerr.
"""

import sys
import os

if len(sys.argv) != 2:
   print(USAGE, file=sys.stderr)
   print('', file=sys.stderr)
   exit(1)

datafile = sys.argv[1]

if not os.access(datafile, os.F_OK):
   print('\nData file "%s" does not exist or cannot be read.\n'
         % datafile, file=sys.stderr)
   print(USAGE, file=sys.stderr)
   print('', file=sys.stderr)
   exit(1)

import numpy as np
import matplotlib.pyplot as plt

drows = np.loadtxt(datafile)
wdat = drows.T

#
# compute plot margins
#
xmar = int(abs((wdat[0][-1] - wdat[0][0])/6))
ymar = int(abs(max(wdat[1])/4))

f1, ax1 = plt.subplots()
ax1.set_xlim(wdat[0][0]-xmar, wdat[0][-1]+xmar)
ax1.set_ylim(0,max(wdat[1])+ymar)
# ax1.plot(wdat[0], wdat[1], 'o')
ax1.errorbar(wdat[0],wdat[1],yerr=wdat[2],fmt='o', capsize=3)
f1.show()

input("\nPress <Enter> to exit...\n")
