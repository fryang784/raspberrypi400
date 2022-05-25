#!/usr/bin/env python3

#
# capfd.py - Discharging capacitor finite difference solution
#
# 03Jun19  Changed variable names
# 06Jun17  Added npoints and switched to object-oriented plotting
# 26May16  Everett Lipman
#

import numpy as np
import matplotlib.pyplot as plt

npoints = 10000

q = np.zeros(npoints)

#
# We calculate these quantities in advance to avoid
# unnecessary computation inside the loop.  
#
dt = 1.0/npoints        # dt = 0.1 ms, t axis runs from 0 to 1.0 s
omdtorc = 1.0 - dt/0.2  # RC = 0.2 s

q[0] = 5.  # initial condition, in microcoulombs

for i in range(npoints - 1):
   q[i+1] = q[i]*omdtorc

f1, ax1 = plt.subplots()
ax1.plot(q)
f1.show()

input("\nPress <Enter> to exit...\n")
