#!/usr/bin/env python3

#
# p3_hw4_generate.py - Execution speed, generate time data for some operations
#
# 21Apr22   Richard Yang
#

# 
# Problem Description:
# 3. Execution Speed. 
# Write a program that uses time.perf counter() to determine how long it takes
# each of the following to execute inside of a loop:
# a. Nothing (a pass statement)
# b. Addition of two float variables
# c. Multiplication of two float variables
# d. Division of two float variables
# e. Integer division of two variables
# f. Appending one number to a list. Does this depend on the length of the 
#    list? get a list of strings as plain string
# g. Call to a function that does nothing (contains only a pass statement)
# h. Call to a function that adds two float variables
# Note: for each of these, you will need to run the operation many times in a 
#       row and divide the total elapsed time to get an accurate answer.
#

#%% 

import time 

times = [0] * 10                # to save all the times
N = 100                         # loop iteration times, so that can get a more 
                                # accurate measurement per loop

#%% Prelim-check: Does redefining variable for time take significant time?
T3 = time.perf_counter()
T1 = time.perf_counter()
for i in range(N):
    T3 = time.perf_counter()    # updates current time in T3 again
    
T2 = time.perf_counter()
T = (T2 - T1)/N
print('\nPrelim-check: time taken for updating time variable')
print('Time taken per iteration = %.3e' % T)

times[0] = T

#%% Objective a, pass:
T1 = time.perf_counter()        # arbitrary reference time
for i in range(N):              # Choose 2 so that there are two iterations
    # print(i)                  # so that loop does iterate at least once. 
    pass

T2 = time.perf_counter()
T = (T2 - T1)/N
print('\nObjective a: pass')
print('Time taken per iteration = %.3e' % T)

times[1] = T

#%% Objective b, float addition:
a = 0.1                         # A float
b = 0.2                         # Another float
T1 = time.perf_counter()
for i in range(N):
    a + b                       # just float addtion, nothing else
    
T2 = time.perf_counter()
T = (T2 - T1)/N
print('\nObjective b: add two floats')
print('Time taken per iteration = %.3e' % T)

times[2] = T

#%% Objective c, float multiplication:
a = 0.1
b = 0.2
T1 = time.perf_counter()
for i in range(N):
    a * b                       # just float multiplication, nothing else
    
T2 = time.perf_counter()
T = (T2 - T1)/N
print('\nObjective c: multiply two floats')
print('Time taken per iteration = %.3e' % T)

times[3] = T

#%% Objective d, float division:
a = 0.1
b = 0.2
T1 = time.perf_counter()
for i in range(N):
    a / b                       # just float division, nothing else
    
T2 = time.perf_counter()
T = (T2 - T1)/N
print('\nObjective d: divide two floats')
print('Time taken per iteration = %.3e' % T)

times[4] = T

#%% Objective e, integer division:
a = 0.1
b = 0.2
T1 = time.perf_counter()
for i in range(N):
    a // b                       # just integer division, nothing else
    
T2 = time.perf_counter()
T = (T2 - T1)/N
print('\nObjective e: multiply two floats')
print('Time taken per iteration = %.3e' % T)

times[5] = T

#%% Objective f part 1, append to a short list:
l1 = [0]                        # a very short list
T1 = time.perf_counter()
for i in range(N):
    l1.append(0)                # append an element into it
    
T2 = time.perf_counter()
T = (T2 - T1)/N
print('\nObjective f part 1: append into a short list')
print('Time taken per iteration = %.3e' % T)

times[6] = T

#%% Objective f part 2, append to a long list:
l1 = [0] * 10000                # a pretty long list
T1 = time.perf_counter()
for i in range(N):
    l1.append(0)                # append an element into it
    
T2 = time.perf_counter()
T = (T2 - T1)/N
print('\nObjective f part 2: append into a long list')
print('Time taken per iteration = %.3e' % T)

times[7] = T

#%% Objective g, call a function that does nothing:
def doNothing():
    pass                        # a function that does nothing
T1 = time.perf_counter()
for i in range(N):
    doNothing()                 # call the function that does nothing
    
T2 = time.perf_counter()
T = (T2 - T1)/N
print('\nObjective g: call a function that does nothing')
print('Time taken per iteration = %.3e' % T)

times[8] = T

#%% Objective h, call a function that does nothing:
def addd(a,b):
    a + b                       # adds two floats
    
a = 0.1
b = 0.2
T1 = time.perf_counter()
for i in range(N):
    addd(a,b)                   # call the function that adds two floats
    
T2 = time.perf_counter()
T = (T2 - T1)/N
print('\nObjective h: call a function that adds two floats')
print('Time taken per iteration = %.3e' % T)

times[9] = T

#%% Append the output to a file
dataFile = '/home/pi/Documents/phys129/yang_homework/yang_hw4/p3_hw4_data.csv'
times_str = ",".join([str(x) for x in times])   # convert list to csv string
times_str = times_str+'\n'

outfile = open(dataFile, 'a')
outfile.write(times_str)
outfile.close()