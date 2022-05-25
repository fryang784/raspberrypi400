#!/usr/bin/env python3

#
# p3_hw7.py -  Stripchart of temperature from MCP9808 
# 11May22   Richard Yang
#
# Problem Description:
# 3. Temperature Stripchart. 
# Modify your program from the previous stripchart problem so that it displays
# the current temperature measured by the MCP9808
#
# See stripchart in Python directory.
#

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

    def emitter(self):
        while True:
            t = time.perf_counter() - self.t0
            with self.I2C() as i2c:
                sensor = self.ada.MCP9808(i2c)

                Tc = sensor.temperature  # float
                Tf = self.cel2far(Tc) 
                print('%.4f degC  %.4f degF' % (Tc, Tf))

            yield t, Tc

#%%============================================================================
# Script
#==============================================================================
if __name__ == '__main__':
    dt = 0.01
    fig, ax = plt.subplots()
    
    scope = Scope(ax, maxt=10, dt=dt, ada=adafruit_mcp9808, I2C=board.I2C )
    ani = animation.FuncAnimation(fig, scope.update, scope.emitter, interval=dt*1000., blit=True)
    
    plt.show()
