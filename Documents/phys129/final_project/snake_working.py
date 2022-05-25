#!/usr/bin/env python3

#
# snake_working.py - current version of python snake game
#
# Latest Update
# 25May22   custom borders; 
# 25May22   deathOverride
# 24May22   do away with coord
# 24May22   grow, death, special head, made coord redundant
# 22May22   no freeze in movement, clearner exit procedure
# 21May22   threading, slicing for coord; border
# 02May22   original file created by Richard Yang
#

head_choice = 'ant'
mapName = 'border_template.txt'
deathOverride = True 

#%%============================================================================
# Import neccessary modules
#==============================================================================

import time
# import keyboard
import numpy as np
import os
# The followings are for keyboard input
import threading
import sys
import select
import tty
import termios

#%%============================================================================
# Define functions or class
#==============================================================================
def file_readlines(filename):
   """Read text file and return the contents as a list of lines.
   """
   infile = open(filename, 'r')
   inlines = infile.readlines()
   infile.close()
   return(inlines)

###############################################################################
def find_cha(st, cha):
    """Returns the indices of all those characters that are the specified 
       'cha' in a string
    """
    for idx, x in enumerate(st):
        if x == cha:
            yield idx

###############################################################################
def import_borders(fname):
    """Returns custom build borders stored in the .txt file called fname.
       Returns pos-like lists for vertical borders and horizontal ones
       separately.
    """
    inlines = file_readlines(fname)
    ver_ylist = []
    ver_xlist = []
    hor_ylist = []
    hor_xlist = []
    
    for j in range(len(inlines)):
        # return two list objects: one for vertical lines, one for 
        # horizontal lines
    
        row = inlines[j]
    
        index = list( find_cha(row, '|'))
        ver_xlist += index
        ver_ylist += list(j*np.ones(len(index)))
    
        index = list(find_cha(row, '-'))
        hor_xlist += index
        hor_ylist += list(j*np.ones(len(index)))
    
    # Return pos-like list object for vertical and horizontal direction
    
    ver_bor = [np.array(ver_ylist, dtype='int'), \
                np.array(ver_xlist, dtype='int')]
    hor_bor = [np.array(hor_ylist, dtype='int'), \
                np.array(hor_xlist, dtype='int')]

    return ver_bor, hor_bor

###############################################################################
def check_dir(p, p_old):
    """Checks if p goes in the opposite direction of p_old. 
       if opposite, return p_old as output.
    """
    global commandList
    returnOld = False
    if p not in commandList:
        returnOld = True
    elif p == 'd' and p_old == 'a':
        returnOld = True
    elif p == 'a' and p_old == 'd':
        returnOld = True
    elif p == 'w' and p_old == 's':
        returnOld = True
    elif p == 's' and p_old == 'w':
        returnOld = True

    if returnOld:
        return p_old
    else:
        return p

###############################################################################
def borders():
    """Return two lists of two np.arrays specifying the y and x coordinates of 
       the borders
    """
    global X, Y
    
    hor_xlist = []
    hor_ylist = []
    ver_xlist = []
    ver_ylist = []
     
    # the top horizontal edge:
    new_xlist = list(np.linspace(0, X-1, X))
    new_ylist = list((Y-1)*np.ones(len(new_xlist)))
    
    hor_ylist += new_ylist
    hor_xlist += new_xlist
    
    # the bottom horizontal edge:
    new_xlist = list(np.linspace(0, X-1, X))
    new_ylist = list(np.zeros(len(new_xlist)))
    
    hor_ylist += new_ylist
    hor_xlist += new_xlist

    # Combine x and y to make pos-like object:
    hor_bor = [np.array(hor_ylist), np.array(hor_xlist)]
    
    # the left vertical edge:
    new_ylist = list(np.linspace(0, Y-1, Y))
    new_xlist = list(np.zeros(len(new_ylist)))
    
    ver_ylist += new_ylist
    ver_xlist += new_xlist
    
    # the right vertical edge:
    new_ylist = list(np.linspace(0, Y-1, Y))
    new_xlist = list((X-1)*np.ones(len(new_ylist)))
    
    ver_ylist += new_ylist
    ver_xlist += new_xlist
            
    # Combine x and y to make pos-like object:
    ver_bor = [np.array(ver_ylist), np.array(ver_xlist)]

    return ver_bor, hor_bor
    
###############################################################################
# def import_borders( fileName ):
#     """Load a .txt file that draws out the border, and return the ordered bor
#        variable
#     """

###############################################################################
def grow(pos):
    """Grow the snake if actual length is less than snakeLength, then call the 
       rand() for a new food location.
    """
    global snakeLength

    if len(pos[0]) < snakeLength:
        # repeat last pair of pos
        y,x = pos
        y = list(y)
        x = list(x)
        y = y + [y[-1]]
        x = x + [x[-1]]
        # return new pos
        pos = [np.array(y,dtype='int'), np.array(x, dtype='int')]

        # run random number for new food
        rand()

    return pos

###############################################################################
def death():
    """Initiate death sequence.
    """
    global pos, exitStatus

    exitStatus = True
    input('Oops, you died! Max length: %d' %len(pos[0]))
    
###############################################################################
def rand():
    """Uses random number to set the position for food

       food_coord: global list with two arrays (like pos, but each array is 
                   length 1)
    """
    global X, Y, food_coord

    # -2 makes sure the food does not go on the border
    # +1 recenter
    x = int((X-2)*np.random.random()) + 1
    y = int((Y-2)*np.random.random()) + 1
    
    food_coord = [np.array([y], dtype='int'), np.array([x], dtype='int')]

###############################################################################
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
def move_snake(p, pos):
    """Moves the snake based on command p. Includes boundary position handling
       Checks/updates snakeLength and deathStatus.
       pos: list of two 1D arrays (y, x)
    """
    
    global exitStatus, head_ch, food_coord, snakeLength, deathStatus
    global X, Y, ver_bor, hor_bor
    
    # Check if to exit game
    if p == '\x1b': # <Esc> key
        print('Exiting main thread')
        exitStatus = True
        pass
    
    # Get current full coordinates of the snake
    y,  x  = pos    # both are arrays (mutable)

    # Get current head position
    hx = x[0]       # both are integers
    hy = y[0]

    # check if food_coord overlaps with head
    if hy == food_coord[0][0] and hx == food_coord[1][0]:
        # grow the snake
        snakeLength += 1

    # move head to new position
    if p == 'd':
        hx += 1#pos[1][0] += 1
        head_ch = '<'
    elif p == 'a':
        hx -= 1#pos[1][0] -= 1
        head_ch = '>'
    elif p == 'w':
        hy += 1#pos[0][0] += 1             # +1 if y coordinate increase
        head_ch = 'v'
    elif p == 's':
        hy -= 1#pos[0][0] -= 1
        head_ch = '^'

    # Update head character
    if p in ['w','a','s','d']:
        head_ch = head_Dict[p]

    # pop the tail and fill in the gap left by the head's movement
    y = list(y)     # array -> list 
    x = list(x)     # array -> list
    y.pop()         # a list
    x.pop()         # a list
    new_x = [hx] + x
    new_y = [hy] + y

    # Create the new pos
    pos = [np.array(new_y, dtype=int), np.array(new_x, dtype=int)]

    # check if the snake is overlapping with itself 
    pos_arr = np.array([new_x, new_y]).T
    deathStatus = len(np.unique(pos_arr, axis=0)) != len(pos_arr)

    # check if the snake is overlapping with the border
    # combine vertical and horizontal border to one bor list:
    bor = [np.array(list(ver_bor[0]) + list(hor_bor[0])), \
            np.array(list(ver_bor[1]) + list(hor_bor[1]))]
    bor_arr = np.array([list(bor[1]), list(bor[0])]).T

    # convert 2darrays to 1d complex to use np.in1d
    pos_c = pos_arr[:,0] + pos_arr[:,1]*1j
    bor_c = bor_arr[:,0] + bor_arr[:,1]*1j

    deathStatus = any(np.in1d(pos_c, bor_c))

    # checks if the head position is out of bound
    # Note: head is the first element within each x,y arrays
    if pos[0][0] < 1:
        # go back 
        pos[0] += 1

    elif pos[0][0] > Y-2:  # X in older syntax for pos
        # go back
        pos[0] -= 1

    if   pos[1][0] < 1:
        # go back
        pos[1] += 1

    elif pos[1][0] > X-2:  # Y in old syntax for pos
        # go back
        pos[1] -= 1 

    return pos

###############################################################################
def display_coord(pos, food_coord, ver_bor, hor_bor):
    """Converts the np.array coord to a string a text to be printed 
       in the display
    """

    global X, Y, head_ch

    # creates a empty np.array with dtype 'S' and
    # the same size as coord
    
    strArr_temp = [' ']*X
    strArr_temp = [strArr_temp]*Y
    strArr = np.array(strArr_temp)
   
    # flipud all the coordinates to be printed out
    pos = flipud(pos)

    food_coord = flipud(food_coord)

    # For some reason the borders do not need to be flipped?
    # ver_bor = flipud(ver_bor)
    # hor_bor = flipud(hor_bor)

    # Use slicing to display snake:
    strArr[tuple(pos)] = '0'

    strArr[tuple(food_coord)] = 'x'

    # Update head with a special character:
    strArr[tuple([pos[0][0], pos[1][0]])] = head_ch


    # Print borders:
    # top and bottom horizontal rows:
    # hor_bor = [np.array(bor[0][0:2*X]), np.array(bor[1][0:2*X])]
    
    # left and right vertical rows:
    # ver_bor = [np.array(bor[0][2*X: -1]), np.array(bor[1][2*X:-1])]

    # Update strArr:
    strArr[tuple(ver_bor)] = '|'
    strArr[tuple(hor_bor)] = '-'

    # initiate string
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
def clear():
    os.system( 'clear' )

###############################################################################
# Below is for terminal input
###############################################################################
def thethread(threadnum):
    """Each thread runs this function. 
    """
    global p_in, old_settings, exitStatus

    dt = 0.1   # time between each iteration

    i = 0
    
    try:
        tty.setcbreak(sys.stdin.fileno())
        while True:
            # print(str(i), flush=True)   # too many prints may jam the stdout
            i += 1
            if isData(): 
                p_in = sys.stdin.read(1) 
                flush_input()
                # print(str(p_in), flush=True)
    
                if p_in == '\x1b' or exitStatus: 
                    print('Exiting', flush=True)
                    
                    break
                
            time.sleep(dt)
    
    
    finally:            # ensures old tty attributes are always restored
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

###############################################################################
def isData():
    """Checks if there is any input available
    """
    return select.select([sys.stdin], [], [], 0)  ==  ([sys.stdin], [], []) 

###############################################################################
def flush_input():
    """flush keyboard buffer. 
    This prevents input loop from thinking your finger is still on the key even
    after you stopped pressing it.

    See:
    https://rosettacode.org/wiki/Keyboard_input/Flush_the_keyboard_buffer#Python
    """
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys, termios
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

#%%============================================================================
# Script
#==============================================================================

old_settings = termios.tcgetattr(sys.stdin) 

# Start 1 additional thread to handle input:
thr = threading.Thread(target = thethread, args = (0,))
thr.start()


# print('keyboard is up')
# time.sleep(1)

# Main thread handles display
counter = 0
# pos = [1,1]                   # initial [x, y] coordinate
xinit,yinit = (1, 1)           

# Start with snake len = 1:
pos = [np.array([yinit], dtype=int),\
       np.array([xinit], dtype=int)]    # [row, col]
                        # pos is a list object, which supports item assignment
                        # when calling coord with pos, use coord(tuple(pos))
                        # since array indexing prefers tuples

snakeLength = len(pos[0]) 
nap = 0.1
X = 80 #40 #80
Y = 20 #12 #22
dim = (X, Y)
commandList = ['w','s','a','d','\x1b']
head_ch = 'v'

# Initiate empty list for food_coord
food_coord = []
rand()

# Special head character dictionaries:
head_ant = {'w':'v','s':'^','a':'>','d':'<'}
head_zero = {'w':'0','s':'0','a':'0','d':'0'}
head_plus = {'w':'+','s':'+','a':'+','d':'+'}

head_Lib = {'ant':head_ant, 'zero':head_zero, 'plua':head_plus}

head_Dict = head_Lib[head_choice]

# initial head character
head_ch = head_Dict['w']

# Get border coordinates:
if not os.path.exists(mapName):
    # Use default map
    ver_bor, hor_bor = borders()
else:
    ver_bor, hor_bor = import_borders(mapName)

p = 'foo'               # command used for control of snake
p_in = 'foo1'           # updated by keyboard input
p_old = 'foo2'          # last control command
exitStatus = False
deathStatus = False

try:
    while True:
    
        print('counter = %d' %counter)
    
        # check for keyboard input p_in, and return p for actual control 
        p = check_dir(p_in, p_old)

        # move head / position
        pos = move_snake(p, pos)

        if not deathOverride:
            if deathStatus:
                death()

        if exitStatus:
            break
    
        # checks growth?
        pos = grow(pos)
    
        # Creates the string representation of coord, and prints
        display_coord(pos,food_coord, ver_bor, hor_bor)
    
        counter += 1

        # Update p_old
        p_old = p
    
        time.sleep(nap)

        clear() # need to figure out a way to not clear when death
    
finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
