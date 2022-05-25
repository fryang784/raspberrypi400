#!/usr/bin/env python3

#
# p1_hw3.py - Print user inputed string 10 times
#
# 13Apr22   Richard Yang
#

#
# Problem description:
# 1. User input. 
# Write a program that asks the user to enter a string, after which it 
# prints the string 10 times. Print each instance of the string on a 
# separate line.
#

print()

string = input('Enter a string: ')  # prompts user input for a string

print((string + '\n')*10)           # prints the inputed string 10 times 
                                    # with each on a new line 
