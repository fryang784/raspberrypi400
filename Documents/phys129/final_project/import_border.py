#!/usr/bin/env python3

#
# import_border.py - import a .txt file and return the ordered bor object.
#
#
# 25May22  Richard Yang

import numpy as np
import string

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

def display_coord(pos_hor, pos_ver):
    """Converts the np.array coord to a string a text to be printed 
       in the display
    """

    global X, Y 

    strArr_temp = [' ']*X
    strArr_temp = [strArr_temp]*Y
    strArr = np.array(strArr_temp)
   
    # flipud on pos for printing out
    pos_hor = flipud(pos_hor)
    pos_ver = flipud(pos_ver)


    # Use slicing:

    # top and bottom horizontal rows:
    # pos_hor = [np.array(pos[0][0:2*X]), np.array(pos[1][0:2*X])]
    
    # left and right vertical rows:
    # pos_ver = [np.array(pos[0][2*X: -1]), np.array(pos[1][2*X:-1])]

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

###############################################################################
def file_readlines(filename):
   """Read text file and return the contents as a list of lines.
   """
   infile = open(filename, 'r')
   inlines = infile.readlines()
   infile.close()
   return(inlines)

###############################################################################
def find_whitespace(mystring):
    """Returns the indices of all whitespaces in a string
    """
    for idx, x in enumerate(mystring):
       if x in string.whitespace:
            yield idx

###############################################################################
def find_cha(st, cha):
    """Returns the indices of all those characters that are the specified 
       'cha' in a string
    """
    for idx, x in enumerate(st):
        if x == cha:
            yield idx
#%%============================================================================

X = 80
Y = 20

fname = 'border_template.txt'

inlines = file_readlines(fname)

ver_ylist = []
ver_xlist = []
hor_ylist = []
hor_xlist = []

for j in range(len(inlines)):
    # iterate over all rows of inlines
    # return two list objects: one for vertical lines, one for horizontal lines

    row = inlines[j]

    index = list( find_cha(row, '|'))
    ver_xlist += index
    ver_ylist += list(j*np.ones(len(index)))

    index = list(find_cha(row, '-'))
    hor_xlist += index
    hor_ylist += list(j*np.ones(len(index)))

# Return pos-like list object for vertical and horizontal direction

ver_pos = [np.array(ver_ylist), np.array(ver_xlist)]
hor_pos = [np.array(hor_ylist), np.array(hor_xlist)]

# display
display_coord(hor_pos, ver_pos)
