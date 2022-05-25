#!/usr/bin/env python3

#
# p5_hw5.py - Mandelbrot set visualization
# 29Apr22   Richard Yang, 
#
# Problem Description:
# 5. Mandelbrot Set. 
# A complex number c is in the Mandelbrot Set if upon repeated iteration the 
# expression z_(n+1) = z_n**2 + c, with z_0 = 0, does not diverge. In other 
# words, |z_n| remains bounded no matter the value of n. In typical 
# illustrations, the complex plane is shown with the Mandelbrot Set in black 
# and the surrounding points c colored according to the number n of iterations 
# required for | z_n**2 + c | to exceed some chosen value.
# Write a program that plots an interesting region of the complex plane in this
# fashion.
# Note: a region containing the whole set is hardly the most interesting you 
# can choose; try zooming in near the edges. Use a grid of 512x384 pixels, and 
# a limit of 250 iterations per point. In other words, if | z_n**2 + c | is 
# still below some small limit of your choosing (think about what a good choice
# might be) after 250 iterations, assume it is in the set.
# Save your plot as a PostScript file (not .eps) and use the translate and 
# scale operators to center the image on the page at a size that leaves 
# 56-point horizontal margins. A good place to put these commands is 
# immediately following the line
# \%%Page: 1 1
# Convert the PostScript file to PDF using ps2pdf and turn in the PDF file with
#  the code
# and text file for the problem.
# Hints: You will probably find it useful to use a smaller grid until you have 
# debugged and optimized your code. It will also help to include some print 
# statements that notify you of the program’s progress.
# See cmapimg.py in $HOME/physrpi/python/ on your RPi for an example of 
# plotting points with a color map rather than explicit RGB values.

import numpy as np
import matplotlib.pyplot as plt 
from PIL import Image
import os, sys
from datetime import date

date = date.today()
d1 = date.strftime("%d%b%y")

pixels = (512, 384)                 # (x-dim, y-dim), with origin at bottomleft
                                    # and ydir positive going up

N = 250                             # number of iterations
thresh = 2                          # arbitrary threshold

def get_coord(Xlim, Ylim, pixels):
    """ return the meshgrids of x coordinate and y coordinate
    x_cd, y_cd each has shape (pixels[0], pixels[1]). 
    To get the x coordinate at pixel index (10, 0), use x_cd[10,0]
    To get the y coordinate at pixel index (0, 10), use y_cd[0,10]
    The ordering of the bracket is in the conventional cartesian sense.
    Xlim, Ylim, and pixels are all lists of two elements.
    """

    xlin = np.linspace(Xlim[0],Xlim[1], pixels[0])
    ylin = np.linspace(Ylim[0],Ylim[1], pixels[1])

    [x_cd, y_cd] = np.meshgrid(xlin, ylin, indexing='ij')
    return x_cd, y_cd

    
def get_M_map(x_cd, y_cd, N, thresh):
    """ returns the mandelbrot map of the region defined by x_cd and y_cd, with
        maximum number of iteration N, and threshold = thresh
    """
    pixels = x_cd.shape
    M_map = np.zeros(pixels, dtype='uint')     # records the maximum iterations
    z_n = np.zeros(pixels, dtype='complex')
    c = x_cd + 1j*y_cd
    for i in range(N):
        if i %  50 == 0:
            print()
            print('i = %d' %i)
        
        # z_n_abs = np.abs(z_n)
        z_n = z_n**2 + c
        M_map[np.abs(z_n) <= thresh] = i+1
    return M_map, z_n


def display_cmap(pvals):

    plotarr = np.flipud(pvals.transpose())
    Max = np.max(plotarr)
    plotarr = (plotarr/Max)*1000
    
    f1, ax1 = plt.subplots()

    picture = ax1.imshow(plotarr, interpolation='none', cmap='jet')


    ax1.axis('off')

    #
    # draw figure
    #
    f1.show()
    f1.canvas.draw()
    

    print('max of plotarr')
    print(np.max(plotarr))
    
    # save the image if does not already exist
    fname = 'p5_hw5_'+d1+str('_N%d.ps' %N)
    if os.access(fname, os.F_OK):
        print('\nFigure already exists: %s\n\n' % fname, file=sys.stderr)
        
    else: 
        # Save the figure as an eps file:
#        im = Image.fromarray(plotarr, 'RGB')
#        im.save(fname)
        f1.savefig(fname, format='ps')
        print('\nFigure saved as %s\n' % fname)
        pass

    # input("\nPress <Enter> to exit...\n")

   
#%%

Xlim = [0.25, 0.55]
Ylim = [0.2, 0.4]
# Xlim = [0.291, 0.330]
# Ylim = [0.044, 0.016]

while True:

    N = input('Enter iteration numbers: ')
    N = N.strip()
    if N == '':
        print('Exited\n\n')
        break
    N = int(N)

    [x_cd, y_cd] = get_coord(Xlim, Ylim, pixels)

    [M_map, z_n] = get_M_map(x_cd, y_cd, N, thresh)
    
    print('Max value = %d, Min = %d' % (np.max(M_map), np.min(M_map)))
    print('unique of M_map:' + str(np.unique(M_map)))

    display_cmap(M_map)
    
