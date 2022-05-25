#!/usr/bin/env python3

#
# cmapimg.py - Display single-valued image in Python using a colormap
#
# 04May18  Moved square of zeros to upper right for visibility
# 13Jul16  Adapted from newimg.py by Everett Lipman
#

import numpy as np
import matplotlib.pyplot as plt

#
# image size
#
X = 320
Y = 200

#
# array for image data (pixel values): one integer value at each (x,y) point
#
# color is determined from pixel value by the colormap
#
pvals = np.zeros((X,Y), dtype='uint')

xinc = 1000/X
yinc = 1000/Y

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
       pvals[i,j] = i*xinc + j*yinc

#
# example: set some pixels to zero:
#
side = 10
x0 = (29*X)//32 - side
x1 = (29*X)//32 + side
y0 = (17*Y)//20 - side
y1 = (17*Y)//20 + side
pvals[x0:x1, y0:y1] = 0

#
# Transpose and flip rows so that origin is displayed at bottom left,
# with x horizontal and y vertical.
#
# Note: changing pvals later WILL change plotarr!  plotarr is a
# different 'view' of the same data.
#
plotarr = np.flipud(pvals.transpose())

f1, ax1 = plt.subplots()

#
# interpolation='none' shows unaltered pixels at all scales
#
picture = ax1.imshow(plotarr, interpolation='none', cmap='jet')

#
# turn off axis labels
#
ax1.axis('off')

#
# draw figure
#
f1.show()

input("\nPress <Enter> to exit...\n")
