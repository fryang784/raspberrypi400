#!/usr/bin/env python3

#
# p4_hw3.py - read an user inputed file, and output averages by line
#
# 13Apr22   Richard Yang
#

#
# Problem description:
#  4. Read File and Average. 
# Write a program that reads numbers from a user-specified file and prints out 
# their average. The file should contain one number per line.
#
# See: "file_readlines.py" function in $~/physrpi/python/
#
# For demonstration purpose, input the file "p4_hw3.txt" when prompted. 

import sys, os, string

#
# If want to import Lipman's function "file_readlines.py", uncomment the 
# following section:
#
# sys.path.append('/home/pi/physrpi/python/')
# from file_readlines import file_readlines
#

filename = input('Enter filename: ')

if os.access(filename, os.F_OK) == False:   # Check if filename does not exist
    print('\nInput file does not exist: %s\n\n' % filename, file=sys.stderr)
    exit() 

print('\nGetting numbers from file: %s\n' % filename)
#%%
infile = open(filename, 'r')
inlines = infile.readlines()
infile.close()

sum = 0

for i in range(len(inlines)):
    inlines[i] = inlines[i][0:-1]       # Get rid of the '\n'
    
    # To make sure each line only contains a number:
    # Define the union of space and punctuations:
    punct_and_space = set(string.punctuation).union(set(' '))
    if any((c in punct_and_space) for c in inlines[i]):
        print('\nPunctuation or space mark found. \
              File should only contain one number per line.')
        break
    sum += float(inlines[i])      # convert to float
    
avg = sum/len(inlines)
print('Average is %d\n' % avg)
