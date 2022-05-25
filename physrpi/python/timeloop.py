#!/usr/bin/env python3

#
# timeloop.py - Time loop execution.
#
# 12Jul16  Everett Lipman
#

import time

N = 10000000

t0 = time.perf_counter()

for i in range(N):
   pass

elapsed = time.perf_counter() - t0

print()
print('Time elapsed for %d loops: %f s' % (N, elapsed))
print()
