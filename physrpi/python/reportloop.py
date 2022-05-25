#!/usr/bin/env python3

#
# reportloop.py - Loop that reports its progress
#
# 21Apr16  Written by Everett Lipman
#

import time

print('\nStarting...\n')

for i in range(10000):
   if i % 100 == 0:
      print('i: %d' %i)
   time.sleep(0.001)
   
print('\nDone.\n')
   
