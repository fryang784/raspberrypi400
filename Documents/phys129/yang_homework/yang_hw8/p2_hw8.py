#!/usr/bin/env python3

#
# p2_hw8.py - Polynomial Fit 
# 19May22   Richard Yang
#
# Problem Description:
# 2. Polynomial Fits. 
# Write a program that generates a user-specified number N of uniformly 
# distributed random points on a region of the x-y plane, with x and y both 
# running from 0–100. Find fits to the set of points using polynomials of 
# degree 1 (a line), N − 3,
# and N − 1. Turn in an EPS plot of the specified region of the x-y plane 
# showing the set of points and the fit curves, in four different colors. 
# Your program may limit the value of N to some reasonable range, and you may 
# use NumPy functions to do the fitting
# 

xmax = 100
ymax = 100
Nmin = 3
Nmax = 100
Seed = False         # Seed np pseudo random for debugging

#%%============================================================================
# Import necessary modules
#==============================================================================
import numpy as np
import matplotlib.pyplot as plt
from datetime import date

#%%============================================================================
# Functions
#==============================================================================
def careful_int(N):
    """Try to convert string N into an integer, with error handling and 
       some conditions specific to this problem.
    """
    import sys
    
    try: 
        N = int(N)
    except ValueError:
        print("Input must be an integer.", file=sys.stderr)
        print("exiting\n", file=sys.stderr)
        exit(1)
    if N < Nmin:
        print("N must be no smaller than %d." % Nmin, file=sys.stderr)
        print("exiting\n", file=sys.stderr)
        exit(1)
    elif N > Nmax:
        print("N must be no larger than %d." % Nmax, file=sys.stderr)
        print("exiting\n", file=sys.stderr)
        exit(1)
    
    return N

###############################################################################
def get_polyfit(xdata, ydata, deg, xplt=None):
    """Return the y values as the result of polyfit
       Note: It is convenient to use poly1d objects for dealing with 
       polynomials. 

       xplt: optional argument, new x variable for plotting purposes.
    """
    if xplt is None:
        xplt = xdata
    popt = np.polyfit(xdata, ydata, deg)
    p = np.poly1d(popt)         # poly1d object
    y_fit = p(xplt)
    return y_fit


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
N = input('Enter number of random points: ')

N = careful_int(N)

if Seed:
    np.random.seed(1)

# Generate random x,y values
x_rand = xmax*np.random.random(N)       # range: [0,xmax)
y_rand = ymax*np.random.random(N)       # range: [0,ymax)

#
# Get polynomial fit
# Note: it's convenient to uose poly1d objects for dealing with polynomials
#

xfit = np.linspace(0, xmax, 101)        # just for plotting

# Degree 1
deg = 1
yfit1 = get_polyfit(x_rand, y_rand, deg, xplt=xfit)

# Degree N - 3
deg = N - 3
yfit2 = get_polyfit(x_rand, y_rand, deg, xplt=xfit)

# Degree N - 1
deg = N - 1
yfit3 = get_polyfit(x_rand, y_rand, deg, xplt=xfit)

#%%============================================================================
# Plotting
f1,ax1 = plt.subplots()
ax1.scatter(x_rand, y_rand, color='blue', label="random data") 
ax1.plot(xfit, yfit1, color='orange', label="Linear fit")
ax1.plot(xfit, yfit2, color='green', label="N - 3 fit")
ax1.plot(xfit, yfit3, color='violet', label="N - 1 fit")

ax1.set_xlim([0,xmax])
ax1.set_ylim([0,ymax])
ax1.legend(loc="lower right")
ax1.set_title(str("N = %d" % N))
f1.show()

# Save the plot
date = date.today()
d1 = date.strftime("%d%b%y")
fname = 'p2_hw8_'+d1+str('_N%d.eps' %N)
careful_savefig(f1, fname)

input('Press <Enter> to exit ')
