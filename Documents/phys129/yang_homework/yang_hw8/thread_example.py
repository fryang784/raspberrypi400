#!/usr/bin/env python3

#
# thread_example.py - Threading example
# 
# 24May16  Everett Lipman
#

import time
import threading

def thethread(threadnum):
   """Each thread runs this function.
   """
   print('I am thread #%d.' % threadnum)
   print('separate thread actions')
#    for i in range(100*threadnum, 100*threadnum+11, 1):
#       print(i)
#       time.sleep(0.5)
#    time.sleep(10)
   
for j in range(1):
   thr = threading.Thread(target = thethread, args = (j,))
   thr.start()


print('All threads active are: %s' %threading.enumerate())
print('This thread is: %s' %threading.get_ident())
print('This thread is the main thread? %s' %(threading.current_thread() is threading.main_thread())) 
