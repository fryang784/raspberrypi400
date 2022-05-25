#!/usr/bin/env python3

#
# inthist.py - Integer histogram
#
# 04Jun20  Fixed problem with half-bin shift
# 19Jun19  Fixed x axis limits
# 31May18  Everett Lipman
#

import os
import sys
import numpy as np

USAGE="""
usage: %s [file]

       file is a single-column text file containing integers
""" % sys.argv[0]
N_ARGUMENTS = (0,1)
###############################################################################

def usage(message = ''):
   if message != '':
      print(message, file=sys.stderr)

   print(USAGE, file=sys.stderr)

   sys.exit(1)
###############################################################################

def check_arguments():
   """Check command line arguments for proper usage.
   """
   global nargs, progname
   nargs = len(sys.argv) - 1
   progname = os.path.basename(sys.argv[0])
   flag = True
   if nargs != 0 and N_ARGUMENTS[-1] == '*':
      flag = False
   else:
      for i in N_ARGUMENTS:
         if nargs == i:
            flag = False
   if flag:
      usage()
###############################################################################

def inthist(datarray, width=1, xmin=None, xmax=None):
   """Generate an integer histogram.
   """
   f, ax = plt.subplots()

   if xmin == None:
      xmin = datarray.min() - 2
   if xmax == None:
      xmax = datarray.max() + 2

   thebins = np.arange(datarray.min(), datarray.max() + width + 1, width)
   thebins = thebins - 0.5*width

   print(thebins)

   hisdata = ax.hist(datarray, thebins)
   print(hisdata)
   ax.set_xlim((xmin, xmax))
   f.show()
###############################################################################

if __name__ == '__main__':
   check_arguments()

   if len(sys.argv) > 1:
      datafile = sys.argv[1]
      if not os.access(datafile, os.F_OK):
         print('\nData file "%s" does not exist or cannot be read.\n'
               % datafile, file=sys.stderr)
         print(USAGE, file=sys.stderr)
         print('', file=sys.stderr)
         exit(1)

      drows = np.loadtxt(datafile)
      data = drows.T
      dmin = min(data)
      dmax = max(data)
      range = dmax - dmin
      margin = round(0.2*range)
      xmi = dmin - margin
      xma = dmax + margin
   else:
      #
      # two dice, 500 throws
      #
      a = np.random.randint(1, 7, 500)
      b = np.random.randint(1, 7, 500)
      data = a + b
      xmi = 0
      xma = 14
         
   import matplotlib.pyplot as plt

   inthist(data, xmin=xmi, xmax=xma)

   print()

   input('Press enter to exit...')
