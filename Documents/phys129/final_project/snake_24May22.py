#!/usr/bin/env python3

#
# snake_working.py - current version of python snake game
#
# based on foo_for_loop.py
#
# Latest Update
# 24May22   grow, death, special head, made coord redundant
# 22May22   no freeze in movement, clearner exit procedure
# 21May22   threading, slicing for coord; border
# 02May22   original file created by Richard Yang
#

head_choice = 'ant'

#%%============================================================================
# Import neccessary modules
#==============================================================================

import time
import keyboard
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
def coord_init(dim):
    """Constructs the position plane, based on the X size and Y size.
       dim is a list [X, Y]
    """
    X, Y = dim
    coord = np.zeros((Y,X), dtype='int')    # (row, col)
    return coord

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

#     else:
#         pass                    # this stops the snake from moving

    if returnOld:
        return p_old
    else:
        return p

###############################################################################
def grow(pos):
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

        # run random number
        rand()

    return pos

###############################################################################
def death():
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
    """Flip the y values to have proper display orientation
    """
    global Y
    y, x = pos
    y = Y - y -1
    pos = [np.array(y, dtype=int), np.array(x, dtype=int)]

    return pos

###############################################################################
def move_head(p, pos):
    """Moves the pos (position of the head) based on P (local) and p (global). 
       Includes boundary position handling
       pos: (array of y positions, array of x positions)
    """
    
    global exitStatus, head_ch, food_coord, snakeLength, deathStatus
    
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

    # check if there are any overlapping part
    pos_arr = np.array([new_x, new_y]).T
    deathStatus = len(np.unique(pos_arr, axis=0)) != len(pos_arr)

# 
#     x_overlap = len(np.unique(new_x)) != len(new_x)
#     y_overlap = len(np.unique(new_y)) != len(new_y)
#     deathStatus = np.logical_and(x_overlap, y_overlap)
#     if deathStatus:
#         print(new_x)
#         print(new_y)
    # checks if the head position is out of bound
    # Note: head is the first element within each x,y arrays
    # This will trigger death in later version
    # For now, just make the snake stuck there
    if pos[0][0] < 1:
        # Death?    i.e. set some global Death status? 
        deathStatus = True

        # go back 
        pos[0] += 1
    elif pos[0][0] > Y-2:  # X in older syntax for pos
        # Death?
        deathStatus = True

        # go back
        pos[0] -= 1

    if   pos[1][0] < 1:
        # Death?
        deathStatus = True

        # go back
        pos[1] += 1


    elif pos[1][0] > X-2:  # Y in old syntax for pos
        # Death?
        deathStatus = True

        # go back
        pos[1] -= 1 

    return pos


###############################################################################
def print_pos_arr( pos, coord):
    """Updates coord based on pos

       Currently un-used. May be unnecessary.
       input:   # p [str]: movement command;
                pos [(x,y)]: memory for the position of head
                coord [2d array]: coordinate array
    """

    global dim

    X = dim[0]
    Y = dim[1]

    # Write the position of head to coordinate
    # Recreate coord array
    coord = np.zeros((Y,X), dtype='int')

    # Assigns position of the snake into coord
    coord[tuple(pos)] = 1       # array indexing prefers a tuple

    # May need to take ydir upside down
    coord = np.flipud(coord)

    return  coord

def display_coord(pos, food_coord):
    """Converts the np.array coord to a string a text to be printed 
       in the display
    """

    global X, Y, head_ch

    # creates a empty np.array with dtype 'S' and
    # the same size as coord
    
    strArr_temp = [' ']*X
    strArr_temp = [strArr_temp]*Y
    strArr = np.array(strArr_temp)
   
    # flipud on pos for printing out
#     y, x = pos
#     y = Y - y -1
#     pos = [np.array(y, dtype=int), np.array(x, dtype=int)]
    pos = flipud(pos)

    # flipud on food_coord for printing out
    food_coord = flipud(food_coord)


    # Use slicing:
    strArr[tuple(pos)] = '0'

    strArr[tuple(food_coord)] = 'x'

    # Update head with a special character:
    strArr[tuple([pos[0][0], pos[1][0]])] = head_ch


    # Print borders:
    strArr[:,0] = '|'
    strArr[:,X-1] = '|'
    strArr[0,:] = '-'
    strArr[Y-1,:] = '-'
    
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

old_settings = termios.tcgetattr(sys.stdin) # some error during exiting. Hmm...

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
# pos = [np.array([yinit], dtype=int),\
#        np.array([xinit], dtype=int)]    # [row, col]

# Start with snake len = 2:
pos = [np.array([yinit], dtype=int),\
       np.array([xinit], dtype=int)]    # [row, col]
                        # pos is a list object, which supports item assignment
                        # when calling coord with pos, use coord(tuple(pos))
                        # since array indexing prefers tuples

snakeLength = len(pos[0]) 
nap = 0.1
X = 80 #40 #80
Y = 22 #12 #22
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
head_ch = head_Dict['w']

# Initiate coordinate:
coord = coord_init(dim) 

# continuously print:
# Need to figure out a better way to keep acount of the old command
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
        pos = move_head(p, pos)

        if deathStatus:
            death()

        if exitStatus:
            break
    
        # checks growth?
        pos = grow(pos)
    
        # Create the coord that reflects the pos
        coord = print_pos_arr(pos, coord)
        
        # Creates the string representation of coord, and prints
        display_coord(pos,food_coord)
    
        counter += 1

        # Update p_old
        p_old = p
    
        time.sleep(0.1)

        clear() # need to figure out a way to not clear when death
    
finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
