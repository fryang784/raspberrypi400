#!/usr/bin/env python3

#
# temp_analysis.py - Generate plot, curve fit, and 
#                    characteristic time from saved data
#
# 12May22  Richard Yang
# 
# THIS IS NOT FOR GRADING IF YOU ARE HERE YOU ARE IN THE WRONG PLACE
# 

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit as cfit

def file_readlines(filename):
   """Read text file and return the contents as a list of lines.
   """
   infile = open(filename, 'r')
   inlines = infile.readlines()
   infile.close()
   return(inlines)

def careful_savefig(f1, filename, fmt='eps'):
    """Save a figure handle as an file, if the file doesn't yet exist.

       f1: a plt figure handle to be saved
       filename: where the figure will be written
       fmt: format to be saved as, default 'eps'
    """
    import os
    import sys
    if os.access(filename, os.F_OK):
        print('\nOutput file already exists: %s\n\n' % filename, file=sys.stderr)
        return

    f1.savefig(filename, format=fmt)
    print('Figure saved as: %s\n\n' % filename)


data = file_readlines('p6a_hw7_time.txt')   # a string list
data = [float(entry) for entry in data]         # --> a float list
data = np.array(data)                           # --> a numpy array
t = data

data = file_readlines('p6a_hw7_temp.txt')   # a string list
data = [float(entry) for entry in data]         # --> a float list
data = np.array(data)                           # --> a numpy array
indata = data

# raw data plot
f1, ax1 = plt.subplots()
ax1.plot(t, indata)
ax1.set_xlabel('time (s)')
ax1.set_ylabel('temp (Celsius)')
ax1.set_title('raw data')

f1.show()
    
figName = 'p6a_hw7.eps'
careful_savefig(f1, figName)

# 
# Analysis
# 

# Get the data after maximum temperature
maxId = np.argmax(indata)
t = t[maxId:]
indata = indata[maxId:]

# Reset first timepoint to 0
t = t - t[0]

#
# Use scipy.optimize.curve_fit
#

popt, pcov = cfit(lambda t,a,b,k: a + (b-a)*np.exp(-1*k*t), t, indata)

# Use a more densely populated time for better fit plot
t_fit = np.linspace(0, max(t), 1000)
temp_fit = popt[0] + (popt[1]-popt[0])*np.exp(-1*popt[2]*t_fit) 

tau = 1/popt[2]
print('Characteristic time is %.3fs' % tau) 

# Plot fit with data
f2, ax2 = plt.subplots()
ax2.plot(t, indata, color='red', label='data')
ax2.plot(t_fit, temp_fit, color='blue', label='fit')

ax2.set_xlabel('time (s)')
ax2.set_ylabel('temp (Celsius)')
ax2.legend()
ax2.set_title('Exponential decay of temperature')

f2.show()

figName = 'p6b_hw7.eps'
careful_savefig(f2, figName)

input('Press <Enter> to exit...\n')
