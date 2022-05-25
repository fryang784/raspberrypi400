#!/usr/bin/env python3

#
# foo_for_loop.py - Use for loop to update strArr. 
# 02May22   Richard Yang, 
#



import time
import keyboard
import numpy as np


def coord_init(dim):
    """Constructs the position plane, based on the X size and Y size.
       dim is a list [X, Y]
    """
    X = dim[0]
    Y = dim[1]
    coord = np.zeros((Y,X), dtype='int')    # (row, col)
    return coord


def print_pos(p):                       # obsolete
    global counter
    global pos
    if p == 'd':
        pos += 1
    elif p == 'a':
        pos -= 1

    else:
        pass

    if pos < 0:
        pos = 0
    elif pos > 79:
        pos = 79
    string = ['=']*80 + ['\n']
    string = string*15
    string = string + ['=']*(pos)+['_']+['=']*(80-pos-1) +['\n']

    string = string + (['=']*80 + ['\n'])*6

    string = ''.join(string) 
    print()
    print(string)
    counter += 1
    time.sleep(nap)


def print_pos_arr(p, pos, coord):
    """loads in the movement command, p, performs movement on coordinate
       and returns the moved coordinate. 
       input:   p: movement command;
                pos: memory for the position of head
                coord: coordinate 2D array
    """

    global dim

    X = dim[0]
    Y = dim[1]
    
    # move to new position
    if p == 'd':
        pos[0] += 1
    elif p == 'a':
        pos[0] -= 1
    elif p == 'w':
        pos[1] += 1             # +1 if y coordinate increase
    elif p == 's':
        pos[1] -= 1

    else:
        pass

    # checks if the position is out of bound
    if pos[0] < 0:
        pos[0] = 0
    elif pos[0] > X-1:
        pos[0] = X-1

    if   pos[1] < 0:
        pos[1] = 0
    elif pos[1] > Y-1:
        pos[1] = Y-1

    # Write the position of head to coordinate
    # Recreate coord array
    coord = np.zeros((Y,X), dtype='int')
    coord[pos[1]][pos[0]] = 1       # all others = 0   

    # May need to take ydir upside down
    coord = np.flipud(coord)

    return pos, coord

def display_coord(coord):
    """Converts the np.array coord to a string a text to be printed 
       in the display
    """

    X = coord.shape[1]
    Y = coord.shape[0]

    # creates a empty np.array with dtype 'S' and
    # the same size as coord
    
    strArr_temp = ['=']*X
    strArr_temp = [strArr_temp]*Y
    strArr = np.array(strArr_temp)
    # strArr = np.empty_like(coord, dtype='S') #dtype = '<U1'   ?

    # if coord[i][j] = 0, print '='
    # if coord[i][j] = 1, print 'O'
    
    # This does not work. 
    # strArr[coord==0] = ' '  #'=' #' '      
    # strArr[coord==1] = 'O'
    
    # Use nested for loops:
    for i in range(strArr.shape[0]):
        for j in range(strArr.shape[1]):
            if coord[i,j] == 0:
                strArr[i,j] = '='
            elif coord[i,j] == 1:
                print('1 is found!')
                strArr[i,j] = 'O'
    
    
    
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

counter = 0
pos = [1, 1]                    # initial [x, y] coordinate
nap = 0.1
X = 80
Y = 22
dim = [X, Y]


# Initiate coordinate:
coord = coord_init(dim) 


while True:
    time.sleep(nap)
    print('counter = %d' %counter)
    counter += 1
    try:
        if keyboard.is_pressed('q'):
            print('Exited out')
            break
        elif keyboard.is_pressed('d'):
            print()
            print('some action')

            pos, coord = print_pos_arr('d', pos, coord)

            display_coord(coord)


        elif keyboard.is_pressed('a'):
            print()
            print('some action')

            pos, coord = print_pos_arr('a', pos, coord)

            display_coord(coord)


           
        elif keyboard.is_pressed('w'):
            print()
            print('some action')

            pos, coord = print_pos_arr('w', pos, coord)

            display_coord(coord)





        elif keyboard.is_pressed('s'):
            print()
            print('some action')

            pos, coord = print_pos_arr('s', pos, coord)

            display_coord(coord)




        else:
            #print_space()
            #print_pos('')
            print('else statement')
            display_coord(coord)
    except:
        print('something else')
        break
