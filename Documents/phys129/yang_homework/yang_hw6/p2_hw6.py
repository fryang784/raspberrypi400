#!/usr/bin/env python3

#
# p2_hw6.py - Plot sine and cosine function in two colors
# 05May22   Richard Yang
#
# Problem Description:
# 2. Plot Trig Functions. 
# Write a program that plots sin(θ) and cos(θ) as functions of θ in two 
# different colors. Show 2.5 complete periods. Label your axes, and include a 
# title for your plot. Turn in your plot as an EPS file along with your 
# program.
# 

#%%============================================================================
# import necessary modules
#==============================================================================

import numpy as np
import matplotlib.pyplot as plt
import os
import sys

#%%============================================================================
# Script
#==============================================================================


p = 2.5                 # unit: number of revolutions
N = 100                 # number of intervals
x = np.linspace(0,p*2*np.pi, N)
y_sin = np.sin(x)
y_cos = np.cos(x)

#
# compute plot margins
#
xmar = (max(x) - min(x))/6              # use 1/6 of the x domain as
y_sinmar = (max(y_sin)-min(y_sin))/4    # margin for x, and 1/4 of y
y_cosmar = (max(y_cos)-min(y_cos))/4    # range as margin for y
ymar = max(y_sinmar, y_cosmar)

# 
# Plotting
#
f1, ax1 = plt.subplots()
ax1.set_xlim(min(x)-xmar, max(x)+xmar)      # set the appropriate axis limits
ax1.set_ylim(min( min(y_sin), min(y_cos) ) - ymar,\
             max( max(y_sin), max(y_cos) ) + ymar)
ax1.plot(x,y_sin, 'o')
ax1.plot(x,y_cos, 'x')

ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_title('Sine and Cosine')

f1.legend(['y = sin(x)', 'y = cos(x)'], loc='upper right')

f1.show()

#
# Save as eps file
#

fname = 'p2_hw6.eps'
if os.access(fname, os.F_OK):
    print('\nOutput file already exists: %s\n\n' % fname, file=sys.stderr)
    print('Figure not saved.')
else: 
    plt.savefig(fname, format='eps')
    print('Figure saved as: %s\n\n' % fname)

input("\nPress <Enter> to exit...\n")
