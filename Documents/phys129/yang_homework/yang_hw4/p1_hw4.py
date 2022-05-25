#!/usr/bin/env python3

#
# p1_hw4.py - Factorization
#
# 20Apr22   stepsize 2 for prime factor searching; error for array overload
# 19Apr22   Richard Yang
#

# 
# Problem Description:
# 1. Factoring Numbers. Write a problem that: 
# a. Prompts the user to enter an integer
# b. Attempts to convert the input string to an appropriate variable
# c. Continues to prompt the user until the conversion is successful
# d. Prints out the prime factors of the number
# Please note: the point of this problem is to write the fastest possible code,
# not to use sophisticated math. Use only elementary division and/or remainder 
# operations. 
# Do not use a number field sieve, nor any other non-trivial algorithm.
# The TA will test your program on these numbers, among others:
# 9879878778787
# 2348923847938743.
#
# See error_handling.py
#%%

import sys 
import numpy as np

print()

# From error_handling.py
while True:
   instr = input("Please enter an integer: ")   # Objective (a)
   try:                         # Objective (b)
      n = int(instr)
   except ValueError:           # Objective (c)
      print("Your input was not an integer.  Try again.\n", file=sys.stderr)
   else:
      if n <=0 :
          print("Input must be non-negative. Try again.\n", file=sys.stderr)      
          
      else:
          break

print("\n\nThe inputed number is %d.\n\n" % n)

if n == 1:
    print("1 does not have a prime factor.\n")
    sys.exit()

#%% 
# Identify all prime factor candidates 
# Use up to sqrt of n as a smaller region of starting points
factorMax = int(n**0.5)
factorCandidates = list(range(2,factorMax+1))
factorCandidates.append(n)                       # append n itself
#%%
# Remove all numbers not divisible to n
factors = []
for i in factorCandidates:
    if n % i == 0:
        factors.append(i)
        
#%% Get the complement of each factor:
# i.e. if a divides n, then b = n/a is here called a complement, 
# and b is also a factor of n
factors_no_complement = factors
for i in factors_no_complement:
    compl = int(n / i)
    if compl != 1 and compl not in factors:     # ignore trivial case of 1
        factors.append(compl)                   # and make sure list is unique
 
#%% Check if each factor is prime
        
primeFactors = []
# A short list of prime numbers as the starting point:
primeList = np.array([2,3,5,7,9,11,13,17,19,23,29])

for i in factors:
    prime = False
    if i in primeList:
        prime = True
        
    elif any(i % primeList == 0):   # Checks if any element from primeList is a
                                    # divisor of factor i
        continue
    
    else:
        try:
            subfactors = np.arange(primeList[-1]+2, int(i**0.5)+1, 2)
                                    # start from the first prime number after
                                    # primeList, up to and include sqrt of i,
                                    # with stepsize=2 since no need to consider
                                    # even numbers
        except ValueError:
            print('Your number exceeds the maximum size allowed.\n', file=sys.stderr)
            print('Exiting program.\n\n')
            sys.exit()
            
        else:
            if not any(i % subfactors == 0):    # numpy parallel operations
                prime = True        # if factor i is not divisble by any 
                                    # number in the subfactors list, then prime
            
    if prime:
        primeFactors.append(i)
        
print('The prime factors are: %s' % primeFactors)