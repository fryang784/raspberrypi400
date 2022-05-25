#!/usr/bin/env python3

#
# p4_hw7.py - Acquire and store data 
# 11May22   Richard Yang
#
# Problem Description:
# 4. Acquire and Store Data. 
# Write a program that acquires one second of voltages from
# your solar cell at a rate of 920 samples per second.
# a. Turn in an EPS plot of the data.
# b. Have your program write the data to disk as a text file containing one 
# voltage per line. Turn in this data file.
# Hints: See the fastadc.py example program.
# Wave your hand over the solar cell to make the data more interesting.
# 
# See fastadc.py in Python directory
#

ACQTIME = 1.0  # seconds of data acquisition

#    samples per second
#    options: 128, 250, 490, 920, 1600, 2400, 3300.
SPS = 920

#    full-scale range in mV
#    options: 16:256, 8:512, 4:1024, 2:2048, 1:4096, 2/3:6144.
VGAIN = 2 

nsamples = int(ACQTIME*SPS)
sinterval = 1.0/SPS

#%%============================================================================
# Import necessary modules
#==============================================================================
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

#%%============================================================================
# Functions
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

#%%============================================================================
# Script
#==============================================================================
# Initialization

print()
print('Initializing ADC...')
print()

i2c = busio.I2C(board.SCL, board.SDA)

#
# Default ADC IC is ADS1015
# Default address is 0x48 on the default I2C bus
#
ads = ADS.ADS1015(i2c)

# Second and third arguments are the ADC channel pins
channel = AnalogIn(ads, ADS.P2, ADS.P3)

# Gain sets the full-scale range in mV (default +/- 6144).
#    options: 16:256, 8:512, 4:1024, 2:2048, 1:4096, 2/3:6144.
#    Note: input should not exceed VDD + 0.3
ads.gain = VGAIN

# Samples per second
#    options: 128, 250, 490, 920, 1600, 2400, 3300.
#
ads.data_rate = SPS

ads.mode = ADS.Mode.CONTINUOUS

indata = np.zeros(nsamples,'float')
vin = AnalogIn(ads, 2, 3)

#%%============================================================================
# Acquisition

input('Press <Enter> to start %.1f s data acquisition...' % ACQTIME)
print()

t0 = time.perf_counter()

for i in range(nsamples):
   st = time.perf_counter()
   indata[i] = vin.voltage
   while (time.perf_counter() - st) <= sinterval:
      pass

t = time.perf_counter() - t0

xpoints = np.arange(0, ACQTIME, sinterval)

print('Time elapsed: %.9f s.' % t)
print()

f1, ax1 = plt.subplots()

#
# Default plotting style connects points with lines
#
ax1.plot(xpoints, indata)

ax1.set_xlabel('time (s)')
ax1.set_ylabel('Voltage (V)')
ax1.set_title('Solar Cell Voltage fastadc')

#
# Plotting with steps is better for visualizing sampling
#
# ax1.plot(xpoints, indata,'-',drawstyle='steps-post')

f1.show()

#%%============================================================================
# Save

outline = list(indata)                          # convert numpy.array -> list
outline = [str(entry)+'\n' for entry in outline]    # float list -> string list
fileName = 'p5_hw7_data_file.txt'
careful_write(outline, fileName)

figName = 'p5_hw7.eps'
careful_savefig(f1, figName)

input("\nPress <Enter> to exit...\n")
