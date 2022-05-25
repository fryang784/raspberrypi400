#!/usr/bin/env python3

#
# p5_hw7.py - Fourier Analysis
# 11May22   Richard Yang
#
# Problem Description:
# 5. Fourier Analysis. 
# Find a light source with periodic intensity, for example a dimmable LED 
# flashlight, a dimmable phone light app or screen, or a fluorescent room light 
# (some fluorescent lights will work, but others will not).
# a. Using your solar cell and the program you wrote for the previous problem, 
#    record the light from this source. Turn in the data file.
# b. Write a new program that reads the data into a Numpy array from the disk 
#    file and computes the power spectrum of the signal using 
#    matplotlib.mlab.psd() or functions from numpy.fft .
# c. Turn in an EPS plot of the power spectrum, and use it to identify the 
#    fundamental frequency at which the light intensity varies.
# Hints: See the psd spectrum.py and fft spectrum.py example programs.
# You may find it necessary to suppress the zero-frequency (DC) component of the
# power spectrum
#

FTIME = 1       # data acquisition time in seconds
FS = 920        # samples per second 

#%%============================================================================
# Import necessary modules
#==============================================================================
import sys
import time
import numpy as np
import matplotlib.pyplot as plt

#%%============================================================================
# Functions
#==============================================================================
def file_readlines(filename):
   """Read text file and return the contents as a list of lines.
   """
   infile = open(filename, 'r')
   inlines = infile.readlines()
   infile.close()
   return(inlines)

#==============================================================================
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

#==============================================================================
def fft_spectrum(y, FTIME, FS):
    """Returns y's frequency value and the power spectrum using fft.

       y: data to be Fourier Transformed. Assume numpy.array
       FTIME: function range in seconds
       FS: samples per second

       based on fft_spectrum.py in physrpi/python by Lipman
    """
    npts = FTIME*FS     # number of sample points
    
    t = np.linspace(0, FTIME, npts)
    ft = np.fft.fft(y)
    ftnorm = abs(ft)
    ps = ftnorm**2
    xvals = np.fft.fftfreq(len(ps), 1.0/FS)
    return xvals, ps

#%%============================================================================
# Script
#==============================================================================
# Load the data

data = file_readlines('p5_hw7_data_file.txt')   # a string list
data = [float(entry) for entry in data]         # --> a float list
data = np.array(data)                           # --> a numpy array

# Fourier power spectrum
[freq, ps] = fft_spectrum(data, FTIME, FS)

# Suppress DC component around frequency = +- 50Hz
fmin = 50
ps[ np.logical_and(freq<fmin,freq>-1*fmin) ] = 0

#%%============================================================================
# Visualize
f1, ax1 = plt.subplots()

#
# Default plotting style connects points with lines
#
ax1.plot(freq, ps)

ax1.set_xlabel('frequency (Hz)')
ax1.set_ylabel('Magnitude')
ax1.set_title(str('Power spectrum, with +- %d Hz suppressed' % fmin))

f1.show()

#%%============================================================================
# Save

figName = 'p5_hw7_power_spec.eps'
careful_savefig(f1, figName)

input("\nPress <Enter> to exit...\n")
