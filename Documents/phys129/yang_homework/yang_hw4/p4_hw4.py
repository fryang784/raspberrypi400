#!/usr/bin/env python3

#
# p4_hw4.py - Prints out Fibonacci series to a user inputed term
#
# 21Apr22   Richard Yang
#
# Note: the first Fibonacci number is 1, not 0
# 

#
# Problem description:
# 4. Fibonacci Numbers. 
# Write a program that takes as a command line argument a single number n, 
# then prints the first n Fibonacci numbers starting with 1, 1, 2, 3, . . .
# Make sure your output has no more than 75 characters per line. You may limit 
# the output to numbers with 75 or fewer digits. 
# Avoid recursion; it can be inefficient in Python.
#

#%%

import sys 

print()

print('Welcome to Fibonacci number generator!\n')

while True:
    n = input('Enter the number of terms you want to display up to: ')
    n = n.strip()
    try:
        n = int(n)
    except ValueError:
        print('Input must be a natural number!\n', file=sys.stderr)
    else:   
        if n <=0 :
            print("Input must be a natural number!\n", file=sys.stderr)      
          
        else:
            break
        
#%% Generate Fibonacci number

# Initialize a list with 3 slots, which is called a cart here:
cart = [1,1,2] 

if n <= 3:
    for i in range(n):
        print(cart[i])
else:
    pass

    # if n >= 4:  
    for i in range(3):
        print(cart[i])
    
    for i in range(n - 3):
        cart[0] = cart[1]               # Move the last two elements to the  
        cart[1] = cart[2]               # first two slots
        cart[2] = cart[0] + cart[1]     # Stores the sum in the 3rd slot
        print(cart[2])
        # stops if number has more than 75 digits:
        if len(str(cart[2])) > 75:
            print('Maximun digits reached (75)')
            print('Ending session...\n\n')
            break

