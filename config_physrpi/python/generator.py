#!/usr/bin/env python3
#
# generator.py - Example of Python generator
#
# 16May18  Everett Lipman
#
"""
Demonstrate a Python generator.

usage: generator.py
"""
import time
import numpy as np

t0 = time.perf_counter()

def gen_ex(p=0.5):
   for i in range(10):
      t = time.perf_counter() - t0
      v = np.random.rand(1)
      if v > p:
         yield 1e6*t, 0.
      else:
         yield 1e6*t, float(np.random.rand(1))

for i in gen_ex(0.5):
   print(i)
