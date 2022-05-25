#!/usr/bin/env python3

#
# p7_hw3_backup.py - Takes a string from user, and output the processed version
#
# 16Apr22   Archived. Please see p7_hw3.py
# 14Apr22   Richard Yang
#

#
# Problem description:
#  7. String Processing. Write a program that
# a. Prompts the user for a string with at least 3 words
# b. Rejects the string and reprompts if the string has fewer than three words
# c. Prints the words in the string, one per line
# d. Prints the first three characters of the string
# e. Prints the last three characters of the string (not counting the newline 
#    character)
# f. Prints the first half of the string (include any characters on the 
#    boundary)
# g. Prints the last half of the string (include any characters on the 
#    boundary)
# h. Prints the string with the words in reverse order
# i. Prints the string with the words alphabetized
# j. Prints each character in the string, one per line
# k. Prints hexadecimal values for each character in the string, one line per 
#    character
#    [Hint: read about the ord() function.]
#

print()

print('Please include at least three words in your string\n')

# Objective (a)
string = input('Enter a string: ')

string_split = string.split()
string_reverse = string.split()   # placeholder. Will get updated in for loop
string_sorted = string.split()    # placeholder. Will get updated in for loop

# Objective (b)
if len(string_split) < 3:   # Check if the string has at least three words
    print('\nString must include at least three words.\n')
    print('\nProgram exited.\n\n')
    exit()                  # Rejects string if fewer than three words
else:
    # Objective (c)
    print('\n(c) Printing the words in the string, one per line:\n')
    for i in range(len(string_split)):
        print(string_split[i])
        # (h) Reverse the order of each word
        string_reverse[i] = string_reverse[i][::-1]
                            # -1 means stepsize is going 1 step backward
        
        # (i) Alphabetize each word
        string_sorted[i] = ''.join(sorted(string_sorted[i]))
                            # sorted will output a list with the characters 
                            # in alphabetical order
                            # ' '.join will join the list with a space

# Objective (d)
print('\n(d) Printing the first three characters of the string:\n')
print(string[0:3])

# Objective (e)
print('\n(e) Printing the last three characters of the string:\n')
print(string[-3:])

# Objective (f)
print('\n(f) Printing the first half of the string (include any characters on \
the boundary)\n')
print(string[0:round((len(string)/2) + 0.1)])
                            # the 0.1 is to make sure Python rounds up. 
                            # for some reason, Python thinks round(2.5) = 2
# Objective (g)
print('\n(g) Printing the last half of the string (include any characters on \
the boundary)\n')   
print(string[round(len(string)/2):])        

# Objective (h)
print('\n(h) Printing the string with the words in reverse order\n')      
print(' '.join(string_reverse))     # joins the list with a space in between    

# Objective (i)
print('\n(i) Printing the string with the words alphabetized\n')        
print(' '.join(string_sorted))      # joins the list with a space in between
       
# Objective (j)
print('\n(j) Printing each character in the string, one per line\n')
for i in string:
    print(i)
    
# Objective (k)
print('\n(k) Printing hexadecimal values for each character in the string, one\
 line per character\n')
for i in string:
    print(format(ord(i), 'x'))      # ord gives the ASCII key for the character
                                    # format with specification 'x' returns 
                                    # hexadecimal value of that number
        
# Session ended
print('\nSession ended.\n\n')