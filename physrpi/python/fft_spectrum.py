#!/usr/bin/env python3

#
# fft_spectrum.py - Demonstrate power spectrum from discrete fft
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

t = np.linspace(0, FTIME, npts)
y = np.sin(2.0*np.pi*f1*t) + 0.5*np.cos(2.0*np.pi*f2*t)
f1, ax1 = plt.subplots()
ax1.plot(t,y)
f1.show()

ft = np.fft.fft(y, n=16*npts)
ftnorm = abs(ft)
ps = ftnorm**2
xvals = np.fft.fftfreq(len(ps), 1.0/FS)
f2, ax2 = plt.subplots()
ax2.plot(xvals,ps)
ax2.set_xlim(0,10)
f2.show()

input("\nPress <Enter> to exit...\n")
