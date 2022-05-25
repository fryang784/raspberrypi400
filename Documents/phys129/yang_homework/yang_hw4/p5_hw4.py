#!/usr/bin/env python3

#
# p5_hw4.py - Sine function with numerical approximations
#
# 22Apr22   Richard Yang
#
# Problem Description:
# 5. Sine Function. 
# Write a program that:
# a. Prompts the user for a non-zero angle in degrees
# b. Continues to reprompt the user unless the input is acceptable
# c. Prompts the user for a number, ≤ 25, of terms to sum in a series
# d. Continues to reprompt the user unless the input is acceptable
# e. Calculates, using a function you have defined called sind(), the sine of 
#    the angle provided by the user. This function must sum a series to the
#    number of terms requested, and may not use any predefined Python math
#    functions.
# f. Calculates the sine of the angle using math.sin()
# g. Prints out a quantitative comparison between the two answers including the 
#    ratio and the absolute difference.
#

#%% Define function 

def fact(a):
    """Computes the factorial for an non-negative integer"""
    ans = a
    if ans == 0:
        ans = 1
    while a > 1:
        ans = ans * (a-1)
        a += -1
    return ans

# Taylor series of sin(x) at x=0:
# x - x**3/(fact(3)) + x**5/(fact(5)) - x**7 / fact(7) + ...


def sinFunc2(n):
    """Write out recursively the Taylor series of sin(x), as a string"""
    expression = ''
    for i in range(n):
        # print('%d, %d' %(i, 2*i+1))
        expression += str('+(%d)*x**%d/(fact(%d))' %((-1)**i, 2*i+1, 2*i+1 ))
        # print(expression)
    return(str(expression))

# Define function that converts angle to approriate value, and then call on 
# sinFunc2(n)
def sind(x, n):
    """Converts inputed angle in Radians to interval [-pi/2, pi/2], such that 
       Taylor series will always work with minimal error"""
    if abs(x) >= 2*math.pi:                     # convert to [-2pi,2pi] range
        x = x - int(x/(2*math.pi))*(2*math.pi)   

    if abs(x) >= math.pi:                       # convert to [-pi,pi] range
        x = x - 2*int(x/math.pi)*math.pi         

    if  x > math.pi/2:                          # mirror to within [0, pi/2]
        x = math.pi/2 - (x - math.pi/2)
        
    elif x < -1*math.pi/2:                      # mirror to within [-pi/2, 0]
        x = -1*math.pi/2 + (-1*math.pi/2 - x)

    # return(x)           
    
    return eval(sinFunc2(n))


#%%

import math, sys

print()

print('Welcome to numerical sine calculator!\n')
exitStatus = False

while True:
    print('(use <e> to exit)\n')
    while True:
        Theta = input('Enter an angle in Degrees: ')
        Theta = Theta.strip()
        if Theta.lower() == 'e':
            print('Exiting the program...')
            exitStatus = True
            break
        else:
            try:
                Theta = float(Theta)
            except ValueError:
                print('Angle must be a number!\n', file=sys.stderr)
            else: 
                if Theta == 0:
                    print('Angle must be non-zero!\n', file=sys.stderr)
                else:
                    Theta = (Theta/180) * math.pi   # Convert to Radians
                    break
    if exitStatus:
        break                   # exits out the program 
    else:
        pass
    
    while True:
        N = input('Enter number of terms to sum ( <= 25): ')
        N = N.strip()
        if N.lower() == 'e':
            print('Exiting the program...')
            exitStatus = True
            break
        else:    
            try:
                N = int(N)
            except ValueError:
                print('Number must be a natural number!\n')
                
            else:
                if N <= 0:
                    print('Number must be a natural number!\n')
                elif N > 25:
                    print('Number must be less than or equal to 25!\n')
                else:
                    break
    
    if exitStatus:
        break                   # exits out the program
    else:
        print('Approximate using self-defined func up to %d terms:' %N)
        sinN = sind(Theta,N)
        print(sinN)
        print('Result using math.sin func: ')
        sinMath = math.sin(Theta)
        print(sinMath)
        print()
        sinDiff = sinN-sinMath
        print('Absolute difference = %.3e' % abs(sinDiff))
        sinPercentErr =  sinDiff/sinMath
        print('Percent error from math.sin = %.3f %%' %(sinPercentErr*100))
    
    
    
    print('Try again?\n')
    