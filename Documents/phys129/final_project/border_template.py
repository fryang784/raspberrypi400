#!/usr/bin/env python3

#
# border_template.py - to play with printing borders
#
#
# 24May22  Richard Yang

import numpy as np

def flipud(pos):
    """Flip the y values to have proper display orientation.
       pos: list of two 1D arrays (y, x)
    """
    global Y
    y, x = pos
    y = Y - y -1
    pos = [np.array(y, dtype=int), np.array(x, dtype=int)]

    return pos
###############################################################################

def display_coord(pos):
    """Converts the np.array coord to a string a text to be printed 
       in the display
    """

    global X, Y 

    strArr_temp = [' ']*X
    strArr_temp = [strArr_temp]*Y
    strArr = np.array(strArr_temp)
   
    # flipud on pos for printing out
    pos = flipud(pos)


    # Use slicing:

    # top and bottom horizontal rows:
    pos_hor = [np.array(pos[0][0:2*X]), np.array(pos[1][0:2*X])]
    
    # left and right vertical rows:
    pos_ver = [np.array(pos[0][2*X: -1]), np.array(pos[1][2*X:-1])]

    # Update strArr:
    strArr[tuple(pos_ver)] = '|'
    strArr[tuple(pos_hor)] = '='

    string = ''

    for i in range(Y):
        # get a list of a strings that belong to a row
        # row = [x.decode('utf8') for x in strArr[i]] 
        row = list(strArr[i])
        
        # convert list to string 
        row = ''.join(row)
        row += '\n'
        string += row

    print()
    print(string)




X = 80
Y = 20

xlist = []
ylist = []
 
# the top horizontal edge:
new_xlist = list(np.linspace(0, X-1, X))
new_ylist = list((Y-1)*np.ones(len(new_xlist)))

ylist += new_ylist
xlist += new_xlist

# the bottom horizontal edge:
new_xlist = list(np.linspace(0, X-1, X))
new_ylist = list(np.zeros(len(new_xlist)))

ylist += new_ylist
xlist += new_xlist

# the left vertical edge:
new_ylist = list(np.linspace(0, Y-1, Y))
new_xlist = list(np.zeros(len(new_ylist)))

ylist += new_ylist
xlist += new_xlist

# the right vertical edge:
new_ylist = list(np.linspace(0, Y-1, Y))
new_xlist = list((X-1)*np.ones(len(new_ylist)))

ylist += new_ylist
xlist += new_xlist
        
# Combine x and y to make pos:
pos = [np.array(ylist), np.array(xlist)]

#%%============================================================================

display_coord(pos)

# input('Enter to exist... ')
