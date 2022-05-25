#!/usr/bin/env python3

import sys
import select
import tty
import termios

def isData():
    """Checks if there is any input available
    """
    val = select.select([sys.stdin], [], [], 0) 
    boo = val == ([sys.stdin], [], []) 
    # print(val)
    # return boo
    return select.select([sys.stdin], [], [], 0)  ==  ([sys.stdin], [], []) 


old_settings = termios.tcgetattr(sys.stdin)
i = 0

try:
    tty.setcbreak(sys.stdin.fileno())
    while True:
        print(i)
        i += 1
        Boo = isData()
        if Boo: 
            c = sys.stdin.read(1)
            print(type(c))
            if c == '\x1b': # 
                print('Exiting')
                
                break


finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
