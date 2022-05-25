#!/usr/bin/env python3

#
# img.py - Display RGB image in Python
#
# 25Apr20  Added call to f1.canvas.draw() to prevent problem with draw_artist()
# 13Jul16  Updated to use object-oriented interface to matplotlib
#          and function reliably when X and Y are changed
# 05May16  Everett Lipman
#

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import time

#
# image size
#
X = 320
Y = 200

#
# array for image data (pixel values): x,y,color[0:2]
#
# color is (r,g,b).
#    Each color level is specified using an 8-bit unsigned integer (0-255)
#
pvals = np.zeros((X,Y,3), dtype='uint8')

rinc = 255/X
binc = 255/Y
stripetop1 = int(Y/2 + Y/20)
stripebot1 = int(Y/2 - Y/20)
stripetop2 = int(0.8*Y + Y/20)
stripebot2 = int(0.8*Y - Y/20)

#
# Note that arrays are typically indexed using entries
# (i,j), where i is the row (vertical) and j is the column
# (horizontal).  This is different from addressing points
# (x,y) in the plane, where x, the first variable, indicates
# horizontal position, and y, the second, indicates vertical
# position.  To make i correspond with x and j with y, we
# will transpose the pvals matrix below before displaying it.
# Furthermore, it is customary in raster graphics for the
# vertical dimension to increase downward from the upper
# left-hand corner of the screen, while in typical x,y plots
# the vertical dimension increases upward from the origin
# at the lower left.  So we also flip the entries along
# the vertical axis using np.flipud() before displaying.
# This way the pixels (i,j) we assign in the array correspond
# to the way we typically think of points in the x,y plane.
#
for j in range(Y):
   for i in range(X):
       pvals[i,j,0] = i*rinc  # red
       pvals[i,j,1] = 0x33    # green
       pvals[i,j,2] = j*binc  # blue

#
# example: set pixel to white
#
pvals[X//32,Y//20,:] = 0xff

#
# Transpose and flip rows so that origin is displayed at bottom left,
# with x horizontal and y vertical.
#
# Note: changing pvals later WILL change plotarr!  plotarr is a
# different 'view' of the same data.
#
# axes (0,1,2) transposed to (1,0,2), so x and y get interchanged.
#
plotarr = np.flipud(pvals.transpose(1,0,2))

f1, ax1 = plt.subplots()

#
# interpolation='none' shows unaltered pixels at all scales
#
picture = ax1.imshow(plotarr, interpolation='none')

#
# turn off axis labels
#
ax1.axis('off')

#
# draw figure
#
f1.show()
f1.canvas.draw()

#
# update image while drawing stripe
#
for i in range(320):
   pvals[i,stripebot1:stripetop1,:] = 0xff  # r,g,b all 255 (white)
   picture.set_data(plotarr)
   ax1.draw_artist(picture)
   f1.canvas.blit(ax1.bbox)

#
# a lot faster not to update and to use slicing instead of a loop
#
pvals[:,stripebot2:stripetop2,:] = (0,0,0xff)  # blue
picture.set_data(plotarr)
ax1.draw_artist(picture)
f1.canvas.blit(ax1.bbox)

#
# save image to TIFF file foo.tif
#
im = Image.fromarray(plotarr, 'RGB')
im.save('foo.tif')

input("\nPress <Enter> to exit...\n")
