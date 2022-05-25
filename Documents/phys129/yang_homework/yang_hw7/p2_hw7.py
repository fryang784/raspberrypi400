#!/usr/bin/env python3

#
# p2_hw7.py -  Stripchart of sine function 
# 10May22   Richard Yang
#
# Problem Description:
# 2. Stripchart. 
# Modify the example program stripchart.py to produce a continuously running 
# plot of sin(ωt) vs. t, with ω = π rad/s.
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

#%%============================================================================
# Define class
#==============================================================================
class Scope(object):
    def __init__(self, ax, maxt=2, dt=0.02, w=np.pi):
        self.ax = ax
        self.dt = dt
        self.maxt = maxt
        self.w = w
        self.tdata = np.array([])
        self.ydata = np.array([])
        self.t0 = time.perf_counter()
        self.line = Line2D(self.tdata, self.ydata)
        self.ax.add_line(self.line)
        self.ax.set_ylim(-1.1, 1.1)
        self.ax.set_xlim(0, self.maxt)
        self.ax.set_xlabel('time (s)')
        self.ax.set_ylabel('y')
        self.ax.set_title(r'y = sin($\pi$*t)')

    def update(self, data):
        t,y = data
        self.tdata = np.append(self.tdata, t)
        self.ydata = np.append(self.ydata, y)
        self.ydata = self.ydata[self.tdata > (t-self.maxt)]
        self.tdata = self.tdata[self.tdata > (t-self.maxt)]
        self.ax.set_xlim(self.tdata[0], self.tdata[0] + self.maxt)
        self.ax.figure.canvas.draw()
        self.line.set_data(self.tdata, self.ydata)
        return self.line,

    def emitter(self):
        while True:
            t = time.perf_counter() - self.t0
            v = np.sin(self.w*t)
            yield t, v

#%%============================================================================
# Script
#==============================================================================
if __name__ == '__main__':
    dt = 0.001
    w = np.pi 
    fig, ax = plt.subplots()
    scope = Scope(ax, maxt=10, dt=dt, w=np.pi)
    ani = animation.FuncAnimation(fig, scope.update, scope.emitter, interval=dt*1000., blit=True)

    plt.show()
