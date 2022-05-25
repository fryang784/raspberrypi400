#!/usr/bin/env python3

#
# cuplot.py - Continuously updated plot
#
# 12Mar19  Everett Lipman
#

DEFP = 40.0

USAGE="""
usage: cuplot.py [period]

       period is the cosine oscillation period in seconds.
       Default is %.1f.
""" % DEFP

INTERVAL = 0.5  # Plotting interval in seconds
RUNLENGTH = 300
AXLIM = 1.2

import os
import sys
import time
import threading
import numpy as np
###############################################################################

if len(sys.argv) == 1:
   period = DEFP
else:
   try:
      period = float(sys.argv[1])
   except:
      print(file=sys.stderr)
      print(USAGE, file=sys.stderr)
      print(file=sys.stderr)
      exit(1)

print()
print('Setting period to %.1f s' % period)

omega = 2.0*np.pi/period

print()
print('Initializing plot window...')
print()

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

plotdata = np.zeros(RUNLENGTH) - 2.0*AXLIM  # initial points outside of window
xaxis = np.arange(RUNLENGTH)
fig, ax = plt.subplots()
ax.set_xlim(0, RUNLENGTH)
ax.set_ylim(-AXLIM, AXLIM)
line = Line2D(xaxis, plotdata, linestyle='None', marker='o')
ax.add_line(line)
fig.show()

#
# Initialize counters and time
#
dpos = 0
rollcounter = 0
t0 = time.perf_counter()
t = time.perf_counter() - t0

#
# Continuous plotting loop
#
while(True):
   pointn = rollcounter*RUNLENGTH + dpos
   nextpoint_time = pointn*INTERVAL
   while (t < nextpoint_time):  
      time.sleep(0.1*INTERVAL)
      t = time.perf_counter() - t0
   
   cosval = np.cos(omega*nextpoint_time)
   plotdata[dpos] = cosval
   dpos = dpos + 1
   if dpos == RUNLENGTH:
      dpos = 0 
      rollcounter = rollcounter+1

   line.set_data(xaxis, plotdata) 
   fig.canvas.draw()  
   
   print('Point #%d  t: %.1f  cos(%.3f*t): %.3f' % (pointn, nextpoint_time,
                                                    omega, cosval))
