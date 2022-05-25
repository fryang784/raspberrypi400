#!/usr/bin/env python3

#
# fork_example.py - fork() example
# 
# 24May16  Everett Lipman
#

import os
import time

retval = os.fork()
child = (retval == 0)

mypid = os.getpid()

if child:
   print('I am the child.  PID: %d.' % mypid)
#   for i in range(100,111,1):
#      print(i)
#      time.sleep(0.5)
else:
   print('I am the parent.  PID: %d.  My child has PID %d.' % 
         (mypid, retval))
#   for i in range(0,11,1):
#      print(i)
#      time.sleep(0.5)

time.sleep(10)
