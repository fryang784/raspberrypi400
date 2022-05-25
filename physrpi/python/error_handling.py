#!/usr/bin/env python3

#
# error_handling.py - Demonstrate error handling.
#
# 26Apr18  Added else statements to try/except constructs
# 27Apr17  Fixed some variable types
# 30Jun16  Everett Lipman
#

import sys

print()

instr = input("Please enter a number: ")
x = float(instr)
print("This line is not reached unless the input is a number.")

# try:
#    x = float(instr)
# except ValueError:
#    print("Your input was not a number.", file=sys.stderr)
#    print("exiting", file=sys.stderr)
#    exit(1)
# 
# print()
# print("The number is: %3g" % x)
# print()

# done = False
# while not done:
#    instr = input("Please enter a number: ")
#    try:
#       x = float(instr)
#    except ValueError:
#       print("Your input was not a number.  Try again.\n", file=sys.stderr)
#    else:
#       done = True
# print("\n\nThe number is %3g.\n\n" % x)

# while True:
#    instr = input("Please enter an integer: ")
#    try:
#       n = int(instr)
#    except ValueError:
#       print("Your input was not an integer.  Try again.\n", file=sys.stderr)
#    else:
#       break
# 
# print("\n\nThe number is %d.\n\n" % n)
