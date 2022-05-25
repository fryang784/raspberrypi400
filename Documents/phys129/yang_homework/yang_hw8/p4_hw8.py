#!/usr/bin/env python3

#
# p4_hw8.py - fork and execv
# 19May22   Richard Yang
#
# Problem Description:
# 4. fork() and execv()
# a. From an interactive Python prompt, use os.execv() to execute the ls 
#    command. Explain what you see after the command has finished running.
# b. Write a program that starts counting from 1, printing the next number 
#    every half second. Each time the program reaches a multiple of 10, it 
#    should announce that it is about to fork, and then fork. The child 
#    process should then announce that it is about to execute ls, and then 
#    execute ls -l using os.execv().
# 

#%%============================================================================
# Import 
#==============================================================================
import os
import time

#%%============================================================================
# Script
#==============================================================================
counter = 1

while True:
    print(counter)

    if counter % 10 == 0:
        print('Fork()ing... ')
        
        retval = os.fork()      # creates a copy of the process. 
                                # returns 0 if process is child, 
                                # returns child PID is process if parent

        child = (retval == 0)

        if child:
            print('Executing "ls -l"... ')
            os.execv('/bin/ls', ('-l',))

        # parent continues to live on

    counter += 1
    time.sleep(0.5)
