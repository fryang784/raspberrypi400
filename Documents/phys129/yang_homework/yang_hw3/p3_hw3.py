#!/usr/bin/env python3

#
# p3_hw3.py -  creates a file from user-provided strings
#
# 13Apr22   Richard Yang
#

#
# Problem description:
# 3.  Write File. Write a program that creates a file containing two 
# user-provided strings, one per line.
#
# See: careful write.py function in $~/physrpi/python/
#

import sys, os

#
# If want to import Lipman's function "careful_write.py", uncomment the 
# following section:
#
# sys.path.append('/home/pi/physrpi/python/')
# from careful_write import careful_write
#

filename = input('Enter a filename: ')

if os.access(filename, os.F_OK):        # Checks the filename does not exist
    print('\nOutput file already exists: %s\n\n' % filename, file=sys.stderr)
    exit() 

str_1 = input('Enter first sentence: ')
str_2 = input('Enter second sentence: ')

outlines = [str_1+"\n" , str_2]         # appends '\n' to start the second 
                                        # sentence on a new line

#
# If relying on "careful_write.py", comment out the rest of the code, and 
# uncomment the line immediately after this comment section:
#
                                        
# careful_write(outlines, filename)

outfile = open(filename, 'w')
for i in outlines:
   outfile.write(i)
outfile.close()