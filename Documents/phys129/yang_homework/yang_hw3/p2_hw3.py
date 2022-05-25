#!/usr/bin/env python3

#
# p2_hw3.py - Use subprocess module to print temperature continuously 
#
# 13Apr22   Richard Yang
#

#
# Problem description:
# 2. Processor Temperature.
# (a) write a program that does the following: 
# 1. Use the subprocess module to read the temperature file by running cat.
# 2. Convert the string returned by cat using float(), and divide to get 
#    degrees celsius.
# 3. Print out the temperature once per second in an infinite loop.
#
# See: subproc_ls.py in $~/physrpi/python on your RPI
#

import subprocess, time

print()

TPATH = '/sys/class/thermal/thermal_zone0/temp'

while True:
    output_text = subprocess.check_output(['cat', TPATH], \
                    universal_newlines=True)    # returns a str
    temp = float(output_text)/1000.0            # convert to degree in celsius

    print("current temperature is:", temp)

    time.sleep(1)                               # sleeps for 1 second