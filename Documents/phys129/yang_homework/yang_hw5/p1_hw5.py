#!/usr/bin/env python3

#
# p1_hw5.py - Read csv and plot simple graph
# 25Apr22   Richard Yang, modified from simple_plot.py with more features
#
# Problem Description:
# 1. Wind Speed
# Write a program to read the wind.dat file and plot average wind speed as a 
# function of local time of day. Display the data points separately with error 
# bars, and do not connect them with any lines or curves. Set the axis limits 
# appropriately, label the axes, and include a title. Save a copy of your plot 
# as encapsulated PostScript (.eps) and turn in this file. You can view .eps 
# files with the gv program.
# Hint: Study the simple_plot.py example function in $HOME/physrpi/python/ on
#    your RPi.
# 

USAGE="""
usage: p1_hw5.py datafile

       datafile is a 3-column text file containing numbers x,y,yerr.
       Data will be plotted with error bars of length 2*yerr.
       
       p1_hw5.py modified from simple_plot.py with more features, such as axis
       labels and titles. 
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

drows = np.loadtxt(datafile)            # Load the data as a matrix
wdat = drows.T                          # Transpose of data

#
# compute plot margins
#
xmar = int(abs((wdat[0][-1] - wdat[0][0])/6))   # use 1/6 of the x domain as 
ymar = int(abs(max(wdat[1])/4))                 # margin for x, and 1/4 of y
                                                # range as margin for y
f1, ax1 = plt.subplots()
ax1.set_xlim(wdat[0][0]-xmar, wdat[0][-1]+xmar) # set appropriate axis limits
ax1.set_ylim(0,max(wdat[1])+ymar)
ax1.plot(wdat[0], wdat[1], 'o')         # display data separate from error bar
ax1.errorbar(wdat[0],wdat[1],yerr=wdat[2],fmt='o', capsize=3)
f1.show()

print()
xlabel = input("Enter x-axis label: ")
ylabel = input("Enter y-axis label: ")
title  = input("Enter a title: ")

ax1.set_xlabel (xlabel)
ax1.set_ylabel(ylabel)
ax1.set_title(title)

f1.show()                               # show the updated plot

save = input("\nSave as a eps file? <Y/N> ")
save = save.strip()
save = save.upper()
if save == 'Y':
    fname = input('Enter a file name to be saved: ')
    if os.access(fname, os.F_OK):
        print('\nOutput file already exists: %s\n\n' % fname, file=sys.stderr)
        print('Figure not saved.')
    else: 
        plt.savefig(fname, format='eps')
elif save == 'N':
    print('Figure not saved.')
    pass
else:
    print('Sorry I did not understand you.')
    print('Figure not saved.')

input("\nPress <Enter> to exit...\n")
