#!/usr/bin/env python3

#
# psd_spectrum.py - Demonstrate Welch's average periodogram
#
# 25Jul17  Everett Lipman
#

FTIME = 32       # function range in seconds
FS = 128         # samples per second
npts = FTIME*FS  # number of sample points
f1 = 0.5  # frequency in Hz
f2 = 1.0  # frequency in Hz

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.mlab import psd

t = np.linspace(0, FTIME, npts)
y = np.sin(2.0*np.pi*f1*t) + 0.5*np.cos(2.0*np.pi*f2*t)
f1, ax1 = plt.subplots()
ax1.plot(t,y)
f1.show()

ny, nx = psd(y, NFFT=npts, Fs=FS, pad_to=16*npts)
f2, ax2 = plt.subplots()
ax2.plot(nx,ny)
ax2.set_xlim(0,10)
f2.show()

input("\nPress <Enter> to exit...\n")
