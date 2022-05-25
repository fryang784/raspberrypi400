#!/usr/bin/env python3

#
# p5_hw8.py - Threaded Stripchart. 
# 20May22   Richard Yang
# 
# Problem Description: 
# 5. Threaded Stripchart. 
# Modify your stripchart program from the previous homework set so that it 
# displays the value of a global variable. Have your program spawn a thread
# that continuously prompts the user for a new value and places it in the 
# global variable.
# The chart should then display the most recent number entered. Make sure 
# your program can deal gracefully with non-numeric input.
# Hints: See thread example.py and error handling.py .
# You will have to declare the global variable using the global keyword in 
# your thread function so that the input value is visible to the rest of the 
# program
#

#%%============================================================================
# Import necessary modules
#==============================================================================
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import warnings
import time
# The following is for threading
import threading

#%%============================================================================
# Define class
#==============================================================================
class Scope(object):
    def __init__(self, ax, maxt=2, dt=0.02):
        self.ax = ax
        self.dt = dt
        self.maxt = maxt
        self.tdata = np.array([])
        self.ydata = np.array([])
        self.t0 = time.perf_counter()
        self.line = Line2D(self.tdata, self.ydata)
        self.ax.add_line(self.line)
        self.ax.set_ylim(0, 20)
        self.ax.set_xlim(0, self.maxt)
        self.ax.set_xlabel('time (s)')
        self.ax.set_ylabel('y value')

    def update(self, data):
        # Someway to check if Exit == True:
        if Exit == True:
            plt.close('all')
            exit(0)
        t,y = data
        self.tdata = np.append(self.tdata, t)
        self.ydata = np.append(self.ydata, y)
        self.ydata = self.ydata[self.tdata > (t-self.maxt)]
        self.tdata = self.tdata[self.tdata > (t-self.maxt)]
        ymar = (max(self.ydata) - min(self.ydata))/6.0
        self.ax.set_xlim(self.tdata[0], self.tdata[0] + self.maxt)
        self.ax.set_ylim(min(self.ydata) - ymar, max(self.ydata) + ymar)
        self.ax.figure.canvas.draw()
        self.line.set_data(self.tdata, self.ydata)
        
        return self.line,

    def emitter(self, p=0.1):
        while True:
            t = time.perf_counter() - self.t0
            yield t, Num

###############################################################################
def thethread(threadnum):
    """Each thread runs this function. 
    """
    global Exit, Num
    Exit = False
    Num = 0.0
#     print('The current threads are %s' %threading.enumerate())
#     print('I am thread #%d.' %threadnum)

    while True:
        N = input('Enter number here: ')

        Num = careful_float(N)

###############################################################################
def careful_float(N):
    """Try to convert string N into a float, with error handling and 
       some conditions specific to this problem.
    """
    import sys
    global Exit, Num

    N = N.strip()
    if N == 'q': 
        print("Exiting.")
        Exit = True
        exit(0)
    try: 
        N = float(N)
    except ValueError:
        print("Input must be a float.", file=sys.stderr)
        return Num
        
    Num = N             # only updates Num if N is a float
    return Num

#%%============================================================================
# Script
#==============================================================================
if __name__ == '__main__':
 
    # Start 1 additional thread to handle input:
    thr = threading.Thread(target = thethread, args = (0,))
    thr.start()

    # Main threads handles Matplotlib:
    dt = 0.01
    fig, ax = plt.subplots()
    scope = Scope(ax, maxt=10, dt=dt)
  
    ani = animation.FuncAnimation(fig, scope.update, scope.emitter, \
            interval=dt*1000., blit=True)
    warnings.filterwarnings("ignore")   # Suppresses warnings
    plt.show()
