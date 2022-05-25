#!/usr/bin/env python3

#
# p6_hw7.py - Heat Transfer 
# 12May22   Richard Yang
#
# Problem Description:
# 6. Heat Transfer. 
# Modify the program you used in the previous two problems so that it acquires 
# and saves temperature data from your MCP9808 at a rate of 4 samples per 
# second.
# a. Heat or cool the sensor and record data as it returns to room 
#    temperature. Turn in an EPS plot of the raw data.
# b. Manually select the portion of the data that contains only the heating or 
#    cooling curve, and fit the data to an exponential function. You can do 
#    this manually by trial and error, or with the appropriate Python 
#    functions. 
#    Determine the time constant of the exponential, and turn in an EPS plot 
#    showing the selected data with the fitting function. Plot the data and 
#    fit in different colors.

#%%============================================================================
# Import necessary modules
#==============================================================================
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from scipy.optimize import curve_fit as cfit
# The following modules are for MCP9808
import board
import busio
import adafruit_mcp9808

#%%============================================================================
# Define class and functions
#==============================================================================
class Scope(object):
    def __init__(self, ax, maxt=2, dt=0.02, ada=adafruit_mcp9808, I2C=board.I2C()):
        self.ax = ax
        self.dt = dt
        self.maxt = maxt
        self.ada = ada
        self.I2C = I2C
        self.tdata = np.array([])
        self.ydata = np.array([])
        self.all_t = np.array([])
        self.all_y = np.array([])
        self.t0 = time.perf_counter()
        self.line = Line2D(self.tdata, self.ydata)
        self.ax.add_line(self.line)
        self.ax.set_ylim(0, 20)
        self.ax.set_xlim(0, self.maxt)
        self.ax.set_xlabel('time (s)')
        self.ax.set_ylabel('Temp (Cel)')

    def update(self, data):
        t,y = data
        self.tdata = np.append(self.tdata, t)
        self.ydata = np.append(self.ydata, y)
        self.all_t = np.append(self.all_t, t)
        self.all_y = np.append(self.all_y, y)
        self.ydata = self.ydata[self.tdata > (t-self.maxt)]
        self.tdata = self.tdata[self.tdata > (t-self.maxt)]
        ymar = (max(self.ydata) - min(self.ydata))/6.0
        self.ax.set_xlim(self.tdata[0], self.tdata[0] + self.maxt)
        self.ax.set_ylim(min(self.ydata) - ymar, max(self.ydata) + ymar)
        self.ax.figure.canvas.draw()
        self.line.set_data(self.tdata, self.ydata)

        return self.line,

    def cel2far(self, T):
        """Convert T from Celsius to Fahrenheit
        """
        return(1.8*T + 32.0)

    def emitter(self):

        while True:
            t = time.perf_counter() - self.t0
            with self.I2C() as i2c:
                sensor = self.ada.MCP9808(i2c)

                Tc = sensor.temperature  # float
                Tf = self.cel2far(Tc) 
                print('%.4f degC  %.4f degF' % (Tc, Tf))

            yield t, Tc

#==============================================================================
def careful_savefig(f1, filename, fmt='eps'):
    """Save a figure handle as an file, if the file doesn't yet exist.

       f1: a plt figure handle to be saved
       filename: where the figure will be written
       fmt: format to be saved as, default 'eps'
    """
    import os
    import sys
    if os.access(filename, os.F_OK):
        print('\nOutput file already exists: %s\n\n' % filename, file=sys.stderr)
        return

    f1.savefig(filename, format=fmt)
    print('Figure saved as: %s\n\n' % filename)

#==============================================================================
def careful_write(outlines, filename):
    """Write a list of strings to a file, if the file doesn't yet exist.

       outlines: a list of the strings to be written
       filename: where the strings will be written
    """
    import os
    import sys
    if os.access(filename, os.F_OK):
        print('\nOutput file already exists: %s\n\n' % filename, file=sys.stderr)
        return

    outfile = open(filename, 'w')
    for i in outlines:
        outfile.write(i)
    outfile.close()
    print('\nOutput file saved as %s\n\n' % filename)

#%%============================================================================
# Script
#==============================================================================
if __name__ == '__main__':
    SPS = 4         # samples per second
    dt = 1.0/SPS 
    fig, ax = plt.subplots()
    
    print()
    print('Initializating the stripchart animation...\n')
    print('Press <q> to stop the Animation.\n')
    
    time.sleep(1)

    scope = Scope(ax, maxt=10, dt=dt, ada=adafruit_mcp9808, I2C=board.I2C )
    ani = animation.FuncAnimation(fig, scope.update, scope.emitter, interval=dt*1000., blit=True, repeat=False)
    
    plt.show()

    # 
    # Press 'q' key to stop the animation!
    # If not responding, just close the figure window
    # This is not very elegant, but the rest of the script is executed. 
    # I have spent a long time trying to configure this, but to no avail.
    # 

    #==========================================================================
    print()
    input('Press <Enter> display raw data plot...\n')

    t = scope.all_t
    indata = scope.all_y
    FTIME = max(t)
    t0 = min(t)                 # temp of surrounding 

    # Show the raw plot and save as EPS file
    f1, ax1 = plt.subplots()
    ax1.plot(t, indata)
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('temperature (Celsius)')
    ax1.set_title('raw data')

    f1.show()

    # Save the raw data plot
    figName = 'p6a_hw7.eps'
    careful_savefig(f1, figName)

    # Always save raw data -- THIS IS NOT FOR GRADING I KNOW IT'S JUST A GOOD HABIT 
    fileName = 'p6a_hw7_temp.txt'
    outline = list(indata)                          # convert numpy.array -> list
    outline = [str(entry)+'\n' for entry in outline]    # float list -> string list
    careful_write(outline, fileName)

    fileName = 'p6a_hw7_time.txt'
    outline = list(t)                               # convert numpy.array -> list
    outline = [str(entry)+'\n' for entry in outline]    # float list -> string list
    careful_write(outline, fileName)

    #==========================================================================
    input('Press <Enter> to get the data after maximum temperature.\n')

    # Get the data after maximum temperature
    maxId = np.argmax(indata)
    t = t[maxId:]
    indata = indata[maxId:]

    # Reset first timepoint to 0
    t = t - t[0]

    # Show the plot for sanity check
    f2, ax2 = plt.subplots()
    ax2.plot(t, indata, color='red', label='data')
    
    f2.show()

    #==========================================================================
    input("\nPress <Enter> to exponential fit...\n")

    #
    # Use scipy.optimize.curve_fit
    #
    
    popt, pcov = cfit(lambda t,a,b,k: a + (b-a)*np.exp(-1*k*t), t, indata)

    # a : ambient temperature
    # b : initial temperature
    # k : 1/characteristic time
    
    tau = 1/popt[2]
    print('Characteristic time is %.3fs\n' % tau) 
    
    # Use a more densely populated time for better fit plot
    t_fit = np.linspace(0, max(t), 1000)
    temp_fit = popt[0] + (popt[1]-popt[0])*np.exp(-1*popt[2]*t_fit) 

    
    # Plot fit with data
    ax2.plot(t_fit, temp_fit, color='blue', label='fit')
    
    ax2.set_xlabel('time (s)')
    ax2.set_ylabel('temp (Celsius)')
    ax2.set_title('Exponential decay of temperature')
    ax2.legend()
    
    f2.show()

    # Save the figure
    figName = 'p6b_hw7.eps'
    careful_savefig(f2, figName)


    input("\nPress <Enter> to exit...\n")
