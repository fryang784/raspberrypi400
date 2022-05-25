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



# Pseudo code:
# Use Scope class as defined in p3_hw7.py. Set rate of 4 samples per second

# Change infinite loop under emitter to input dependent condition. Hit a key to stop
# data recording

# Save EPS plot of raw data. Save raw data. (Argue for why the necessary in .txt) 

# Assume heat up and then cools off, so find the maximum temperature and chop 
# everything before

# Determine time constant

# Show EPS plot of selected data with fitting function, Plot data and fit in different colors. 


#%%============================================================================
# Import necessary modules
#==============================================================================
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
# The following modules are for MCP9808
import board
import busio
import adafruit_mcp9808
# The followings are for non-blocking console input
import sys
import select
import tty
import termios

#%%============================================================================
# Define class
#==============================================================================
class Scope(object):
    def __init__(self, ax, maxt=2, dt=0.02, ada=adafruit_mcp9808, I2C=board.I2C()):
        self.ax = ax
        self.dt = dt
        self.maxt = maxt
        self.ada = ada
        self.I2C = I2C
        self.old_settings = termios.tcgetattr(sys.stdin)
        self.tdata = np.array([])
        self.ydata = np.array([])
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

    def isData(self):
        """Checks if there is any input available
        """
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

    def emitter(self):
        # try: 
        # tty.setcbreak(sys.stdin.fileno())

        i = 0
        done = False

        while not done:
            tty.setcbreak(sys.stdin.fileno()) 

            t = time.perf_counter() - self.t0

            if self.isData():
                c = sys.stdin.read(1)
                if c == '\x1b':         # x1b is ESC
                    done = True
                    print('Esc pressed')
            else:
                print('no input')
                print(select.select([sys.stdin], [], [], 0))
                print([sys.stdin], [], [])
            

            print(str(i))
            i += 1
            if i > 30:
                done = True

            with self.I2C() as i2c:
                sensor = self.ada.MCP9808(i2c)

                Tc = sensor.temperature  # float
                Tf = self.cel2far(Tc) 
                print('%.4f degC  %.4f degF' % (Tc, Tf))

            yield t, Tc
        
        # except:
        #     print('Something wrong happened!')
        # finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

#%%============================================================================
# Script
#==============================================================================
if __name__ == '__main__':
    dt = 0.01
    fig, ax = plt.subplots()
    
    # old_settings = termios.tcgetattr(sys.stdin)
    
    scope = Scope(ax, maxt=10, dt=dt, ada=adafruit_mcp9808, I2C=board.I2C )
    ani = animation.FuncAnimation(fig, scope.update, scope.emitter, interval=dt*1000., blit=True, repeat=False)
    
    plt.show()

    print('Some action here!')
