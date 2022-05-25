#!/usr/bin/env python3

#
# p4_hw5.py - plot the same graphic as shown in rt345.eps using python
# 28Apr22   Richard Yang, 
#
# Problem Description:
# 4. 3-4-5 Right Triangle. 
# Examine the code in $HOME/physrpi/ps/rt345.eps on your RPi, and use the gv 
# program to view the result.
# Using what you need from $HOME/physrpi/python/img.py, write a program that 
# draws the same figure using raster graphics (by setting and displaying 
# pixels). Make your image 512 pixels wide. In the text file for this problem, 
# explain how you chose which pixels to set.
# Hint: Look at the bottom of the Handouts section of the course web page for 
# links to the PostScript Language Tutorial and Cookbook and the PostScript 
# Language Reference Manual.
# 
# See img.py
#

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

#%% Setup image property
#
# image size
#
X = 512
Y = 409

#
# array for image data (pixel values): x,y,color[0:2]
#
# color is (r,g,b).
#    Each color level is specified using an 8-bit unsigned integer (0-255)
#
pvals = np.zeros((X,Y,3), dtype='uint8')

# Note that the coordinate for image display in python and for our conventional
# use of cartsian plane are different. In cartesian plane, we write any 
# position as (x,y), and the ydir is increasing going up the page. In python,
# a matrix is called by the order of (row, col), and increasing col number 
# correspond to going downward in the page. Here, I will adopt Lipman's 
# convention, where everything defined in the pvals matrix correspond to 
# conventional cartesian view of (x,y), and a new matrix called "plotarr" 
# will be constructed based on pvals but with its x and y swapped, and its ydir
# going in reverse order, thus conforming to python graphic convention. Note 
# that plotarr is linked to pvals in the sense that any later modification to
# pvals will be reflected in plotarr. 

pvals[:,:,:] = 0xff           # white background

plotarr = np.flipud(pvals.transpose(1,0,2))

f1, ax1 = plt.subplots()

#
# interpolation='none' shows unaltered pixels at all scales
#
picture = ax1.imshow(plotarr, interpolation='none')

ax1.axis('off')                 # turn off axis labels

# draw figure
f1.show()
f1.canvas.draw()

#%% Update image while drawing triangle

color = (0, 0, 0xff)            # blue
half_lw = 10                    # lw = 20, so half of lw is 10

#
# offset is read from the .eps file. p1, p2, and p3 are subsequently defined 
# relative to offset. Note that all points are defined in 2D, 
# i.e. (x,y) = (p1[0], p1[1])
#

offset = np.array([58, 58])     
p1 = offset + np.array([0, 0])
p2 = offset + np.array([400, 0])
p3 = offset + np.array([400, 300])

# two straight legs:
pvals[p1[0]:p2[0], p1[1]-half_lw:p1[1]+half_lw, :] = color
pvals[p2[0]-half_lw:p2[0]+half_lw, p2[1]:p3[1], :] = color

#
# fill the outer gap at the corner of the two legs
# This seems to be the behavior of the .eps file
#
pvals[p2[0]:p2[0]+half_lw, p1[1]-half_lw:p1[1]+half_lw, :] = color

#
# For the hypotenuse, define mutiple masks to segment the region out.
#
# hypov is the vector pointing from p1 to p3
#
hypov = p3 - p1

#
# Find an expression for the hypotenuse, which is a function in 2D cartesian
# We know the slope is (4,3) , and that it passes through p1
#
xlin = np.linspace(0,X-1,X)
xlin = xlin.astype(int)
slope = hypov[1]/hypov[0]
y_mid =  slope*(xlin - p1[0]) + p1[1]

#
# Since the hypotenuse has a line width, we can define translate y_mid up and
# down. Note that since the hypotenuse is tilted, we need to find the 
# projection of a tilted linewidth onto the ydir
#
theta = np.arctan(slope)
half_lw_tilted = abs(half_lw/np.cos(theta))

# y translation for upper bound and lower bound:
y_lower = y_mid - half_lw_tilted
y_higher = y_mid + half_lw_tilted

# Define a set of masks
ylin = np.linspace(0, Y-1, Y)
ylin = ylin.astype(int)

mask1 = np.zeros((X,Y))
mask2 = np.zeros((X,Y))
mask3 = np.zeros((X,Y))
mask4 = np.zeros((X,Y))

for i in range(mask1.shape[0]):
    mask1[i, :] = ylin < y_higher[i]
    mask2[i, :] = ylin > y_lower[i]
    mask3[i, :] = ylin >= (p1[1] - half_lw)
    
for j in range(mask1.shape[1]):
    mask4[:, j] = xlin < (p2[0] + half_lw)

# The mask for hypotenuse is the intersection of all 4 masks:
mask = mask1*mask2*mask3*mask4

pvals[mask.astype(bool), :] = color


#%% Update figure and save:
picture.set_data(plotarr)
ax1.draw_artist(picture)
f1.canvas.blit(ax1.bbox)


fname = 'p4_hw5.eps'   # output file name

# 
# The following save still has one pixel of white space padding, but is the 
# the best out of many that I have tried. This method also preserves the pixel
# size of the saved image.   
#

# Save the figure as an eps file:
im = Image.fromarray(plotarr, 'RGB')
im.save(fname, format='eps')

 
input("\nPress <Enter> to exit...\n")