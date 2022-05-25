#!/usr/bin/env python3

#
# p3a_hw8.py - Monte Carlo Circle: generate
# 19May22   Richard Yang
#
# Problem Description:
# 3. Monte Carlo Circle. (a)
# Write a program that generates a user-specified number N of uniformly 
# distributed random points on a region of the x-y plane with x and y both 
# running from 0–2. By counting the number of points lying within the circle 
# of radius 1 centered at (x, y) = (1, 1), determine the area of this circle 
# and the corresponding value of π.

xmax = 2
ymax = 2
R = 1               # radius of circle
Nmin = 1
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
        
    return N

###############################################################################
def num_in_circle(x, y, R, O):
    """Returns the number as well as the index of 2D points (specified by x
       and y) that lie within the cirlce defined by radius R and center O 
       (a tuple).
    """
    Ox = O[0]
    Oy = O[1]
    InCirc = (x - Ox)**2 + (y - Oy)**2 < R**2   # Bool array

    Num = InCirc.sum()                          # count number of True's
    Index = InCirc.nonzero()                    # array of index for the True's

    return Num, Index

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
# Generate the plot with the circle displayed
x = np.linspace(0, xmax, 2**8)     # 8 bit precision
y = np.linspace(0, ymax, 2**8)
[X, Y] = np.meshgrid(x, y)

while True:
    plt.close('all')                        # close all figures
    f1, ax1 = plt.subplots(figsize=(5,7))   # figsize=(width,height) 
                                            #           unit: inches
    
    # 
    # A Circle is a sub-class of an Patch. We first create the patch.
    #
    Ox = xmax/2
    Oy = ymax/2
    O = (Ox, Oy)                        # Center of circle (tuple)
    circ1 = plt.Circle(O, R, color='b', fill=False)
    
    # Add the patch object to axis
    ax1.add_patch(circ1)                
    
    ax1.set_xlim([0, xmax])
    ax1.set_ylim([0, ymax])
    ax1.set_aspect('equal')              # make the x and y aspect the same
    f1.show()
    
    
    N = input('Enter number of random points: ')
    N = N.strip()
    if N == '':
        break
    
    N = careful_int(N)
    
    if Seed:
        np.random.seed(1)
    
    # Generate random x,y values
    x_rand = xmax*np.random.random(N)       # range: [0,xmax)
    y_rand = ymax*np.random.random(N)       # range: [0,ymax)
    
    # Get number of points inside the circle
    N_in, Id = num_in_circle(x_rand, y_rand, R, O)
    
    # Get the points inside the circle
    x_in = x_rand[Id]
    y_in = y_rand[Id]
    
    # Area estimate
    A = (N_in/N)*4.0
    
    #%%========================================================================
    # Plot the points
    ax1.scatter(x_rand, y_rand, color='orange',label="outside")
    ax1.scatter(x_in, y_in, color='green', label="inside")
    
    ax1.set_xlim([0, xmax])
    ax1.set_ylim([0, ymax])
    ax1.legend(loc='lower right')
    ax1.set_title(str("N = %d" %N))
    
    # Display the area and pi estimate:
    txt=str(r'Area of circle = %d/%d * 4 = %.5f  $\approxeq \pi$ ' \
            %(N_in, N, A))
    f1.text(0.5 ,0.05, txt, ha='center', fontsize=12)
    f1.show()
    
    # Save the plot and the data
    date = date.today()
    d1 = date.strftime("%d%b%y")
    
    fname = 'p3a_hw8_'+d1+str('_N%d.eps' %N)
    careful_savefig(f1, fname)

    input('Press <Enter> for the next figure. ')
