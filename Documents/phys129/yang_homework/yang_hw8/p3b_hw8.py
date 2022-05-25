#!/usr/bin/env python3

#
# p3b_hw8.py - Monte Carlo Circle: error analysis
# 19May22   Richard Yang
#
# Problem Description:
# 3. Monte Carlo Circle. (b)
# Write a second program to plot the fractional error in the determined value 
# of π as a function of N. Turn in the plot as an EPS file.
# 

Nmin = 1
Nmax = 200
Nsamples = 100
R = 1                                 # centered at (1,1)

#%%============================================================================
# Import necessary modules
#==============================================================================
import numpy as np
import matplotlib.pyplot as plt
from datetime import date

#%%============================================================================
# Functions
#==============================================================================
def num_in_circle(x, y, R, O):
    """Returns the number as well as the index of 2D points (specified by x
       and y) that lie within the cirlce defined by radius R and center O 
       (a tuple).
    """
    Ox = O[0]
    Oy = O[1]
    InCirc = (x - Ox)**2 + (y - Oy)**2 < R**2   # Bool array

    Num = InCirc.sum()                          # count number of True's
    # Index = InCirc.nonzero()                    # array of index for the True's

    return Num #,Index

###############################################################################
def percent_error(measured, expected):
    """Returns the absolute value of the percent error between measured value 
       and expected value. 
       percent error = abs(measured - expected) / expected
    """
    per = abs(measured - expected) / expected
    return per
    
###############################################################################
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


#%%============================================================================
# Script
#==============================================================================

intv = (Nmax - Nmin)/Nsamples
counter = 0
N_array = np.zeros(Nsamples)
errors = np.zeros(Nsamples)
for N in np.arange(Nmin, Nmax, intv):
    N = int(N)
    if counter % 5 == 0:
        print(str('Now processing N = %d' %N))

    N_array[counter] = N
    # Generate random x,y values
    x_rand = 2.0*np.random.random(N)       # range: [0,2)
    y_rand = 2.0*np.random.random(N)       # range: [0,2)

    # Get number of points inside the circle
    N_in = num_in_circle(x_rand, y_rand, R, (1.0,1.0))

    # Area estimate
    A = (N_in/N)*4.0

    # Get percent error:
    errors[counter] = percent_error(A, np.pi)

    counter += 1

#%%============================================================================# Plotting

f1, ax1 = plt.subplots()

ax1.plot(N_array, errors, linestyle='dashed')
ax1.scatter(N_array, errors, color='blue')
ax1.set_ylabel('percent error')
ax1.set_xlabel('N')
ax1.set_title(str("Trend of Monte Carlo error, with Nmax = %d" %max(N_array)))

f1.show()

fname = str('p3b_hw8_N%d.eps' %max(N_array))
careful_savefig(f1, fname)

input('Press <Enter> to exit. ')
