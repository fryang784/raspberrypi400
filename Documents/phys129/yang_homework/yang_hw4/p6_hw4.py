#!/usr/bin/env python3

#
# p6_hw4.py - Sine function with numerical approximations
#
# 22Apr22   Richard Yang
#
# Problem Description:
# 6. Julian Day. 
# Download and read the Julian day handout from the course web page. 
# Write a program that
# a. Prompts the user for a date in the form DDMmmYYYY. For example, 26Apr2016.
# b. Computes and prints the Julian day number corresponding to 0 h universal 
#    time on the selected date
# c. Computes and prints the day of the week on which the selected date falls.
# Your program must use separately defined functions to
# a. Prompt the user and return his/her input string
# b. Parse the input string and return a list containing the year, month 
#    number (1–12), and day of the month
# c. Compute the Julian day number using the list returned by the function  
#    from the previous item
# d. Compute the day of the week given the Julian day number
# Use your program to find the day of the week on which you were born, and for 
#    how many days you have been alive.
# Hint: You may want to refer to the online Python documentation for the time 
#    module

#%% Define some functions and basic structures
def help_fun():
    """ Displays the help page for this program
    """
    print('='*80)
    print("Enter a date in Gregorian calendar, in the format 'DDMmmYYYY'")
    print("For instance, the date April 26th, 2016 " + 
          "should be inputed as'26Apr2016'" )
    print("This program will print out the Julian day number " + 
          "corresponding to 0 h universal time on the selected date, " + 
          "and the day of the week on which the selected date falls\n")
    print("(Enter <E/e> to exit program)")
    print('='*80)
        
def exit_fun():
    print('Exiting program...\n')
    print('Bye!\n\n')
    sys.exit()
def GregToJD0h(D, M, Y):
    """Convert from Gregorian date to Julian day, corresponding to 0h 
       universal time (UT) on the inputed date.
       Conversion is done according to the Julian Day handout (pg. 61) by Jean
       Meeus. 
       Arguments: D = days; M = month; Y = year; all integers
    """
    #
    if M > 2:
        pass
    else: 
        M = M + 12
        Y = Y - 1
        
    A = int(Y/100)
    B = 2 - A + int(A/4)
    JD = int(365.25*(Y+4716)) + int(30.6001*(M+1)) + D + B - 1524.5
    # I think this returns the JD at 0h UT. This seems to be consistent with 
    # the Julian Day handout. 
    # The fact that JD will likly have decimal point .5 is because by 
    # convention Julian starts the day at 12h
    
    return(JD)
    
def JD0hToDoW(JD, mode='s'):
    """Returns the day of week corresponding to a given JD, assumed to be at 0h 
       universal time (UT) on selected date
       Arguments:
       JD: Julian day of the selected date
       mode: 's' returns the string of the DoW, i.e. 'Sunday', 'Monday', etc.
             'd' returns the number of that DoW, i.e 'Sunday' = 0, 'Monday' = 1
    """
    DoWTable = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday',
                4: 'Thursday', 5: 'Friday', 6: 'Saturday'}
    
    DoW = int( JD + 1.5 ) % 7
    
    if type(DoW) != int:
        print('JD is not formated at 0h UT!', file=sys.stderr)
        return
    
    if mode=='d':
        return DoW
    elif mode=='s':
        return DoWTable[DoW]
    
month = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
         'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct':10, 'Nov':11, 'Dec':12
         }    

#%% User interactive part:
    
import sys

print()

counter = 0
while True:
    if counter > 3:
        print('(Enter <H/h> to see Help)\n')
        counter = 0
        
    command = input("Enter a date in 'DDMmmYYYY' format: ")
    command = command.strip()
    counter += 1
    
    if command.lower() == 'h':
        help_fun()
        continue
    if command.lower() == 'e':
        exit_fun()
        
    if len(command) != 9:
        print('Input string length incorrect. Check your format.')
        continue

    try:
        Month = month[command[2:5]]
    except KeyError:
        print('Month not found. Check your format.')
        continue
        
    try: 
        Day = int(command[0:2])
    except ValueError:
        print('Day incorrectly formated. Check your format.')
        continue
    else: 
        if Day < 1:
            print('Day must be a natural number!')
            continue
        
    try: 
        Year = int(command[5:9])
    except ValueError:
        print('Year incorrectly formated. Check your format.')
        continue
    else:
        break
    

JD = GregToJD0h(Day,Month,Year)
DoW = JD0hToDoW(JD)
print('The date %02d/%02d/%d (MM/DD/Year) is' %(Month, Day, Year))
print('JD: %.02f, %s' %(JD, DoW))