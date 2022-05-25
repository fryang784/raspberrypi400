#!/usr/bin/env python3

#
# p3_hw6.py - Surface plot
# 05May22   Richard Yang 
#
# Problem description:
# 3. Surface Plot. 
# Write a program using the plot surface method from the Axes3D class to plot 
# the function z(x, y) = sin(x) cos(y). Show 2.5 periods on the x and y axes.
# Turn in your plot as an EPS file along with your program.
# Hint: http://matplotlib.org/3.3.4/tutorials/toolkits/mplot3d.html
#
# See 'surface3d_demo2.py'

#%%============================================================================
# import necessary modules
#==============================================================================

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import sys

#%%============================================================================
# Script
#==============================================================================

#
# Make data
# 
p = 2.5                 # unit: number of revolutions, for both x and y dir
N = 100                 # number of intervals
x = np.linspace(0,p*2*np.pi, N)
y = np.linspace(0,p*2*np.pi, N)
[X, Y] = np.meshgrid(x, y)      # Creates 2D arrays for the meshgrid

# compute Z in parallel
Z = np.multiply(np.sin(X), np.cos(Y))
# Note that X is the x-coordinates of every point in the 2D region define,
# and Y is the y-coordinates of every point in the same region. 
# np.sin and np.cos is able to take inputs that are array-like (apparently of 
# dimension higher than 1D), which computes in parallel on each element. 
# Then, np.multiply performs element-wise multiplication of the two matrices.


# To check that this is indeed what we should expect, uncomment the following 
# code block: 
#==============================================================================
#
# Z_2 = np.zeros(X.shape)           # same shape as X and Y
# 
# #
# # loop over every row of 2D meshgrid
# # Since np.sin and np.cos can take in array-like input, we can use each row of 
# # X and Y as input to these two functions. 
# # This also only works because X, Y, and Z have the same shape
# #
# 
# for j in range(Z_2.shape[0]):       # iterate over rows, i.e. y direction
#     for i in range(Z_2.shape[1]):   # iterate over cols, i.e. x direction
#         Z_2[i,j] = np.sin(X[i,j]) * np.cos(Y[i,j])
# 
# 
# # Compare if Z is equal to Z_2
# 
# AllTrue = ~((Z != Z_2).any())   # any returns True is any of the items is True
#                                 # any returns False is empty or all are false
# print('AllTrue is %s' % AllTrue)
# 
#==============================================================================

#
# Plotting
#
f1 = plt.figure()
ax1 = f1.add_subplot(111, projection='3d')

ax1.plot_surface(X, Y, Z, color='b')

# plot Z_2 on the same axis for comparison
# ax1.plot_surface(X, Y, Z_2, color='r')

ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_zlabel('z')
ax1.set_title('Z = sin(x)*cos(y)')

f1.show()

#
# Save as eps file
#

fname = 'p3_hw6.eps'
if os.access(fname, os.F_OK):
    print('\nOutput file already exists: %s\n\n' % fname, file=sys.stderr)
    print('Figure not saved.')
else: 
    plt.savefig(fname, format='eps')
    print('Figure saved as: %s\n\n' % fname)


input("\nPress <Enter> to exit...\n")
