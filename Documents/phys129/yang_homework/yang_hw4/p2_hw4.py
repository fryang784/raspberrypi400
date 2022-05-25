#!/usr/bin/env python3

#
# p2_hw4.py - Dictionary and Database
#
# 20Apr22   Richard Yang
#

# 
# Problem Description:
# 2. Dictionaries and Databases. 
# Write a program that
# a. Reads in the csv file
# b. Stores the information from the csv file in a list of Python dictionaries,
#    one per line. You should choose the key names, for example 'last', 
#    'first', 'color', etc.
# c. Prints a list of keys for the user
# d. Prompts the user to choose a key
# e. Prints all names in alphabetical order with the requested values. For 
#    example, if the user selects the key 'color', the program should print 
#    something like:
#       Einstein, Albert: green
#       Fermi, Enrico: red
#       Michelson, Albert: blue
#    Hint: create a list of output strings and sort it before printing.
# f. Allows the user to continue selecting keys for display until he/she is 
#    finished.
#

#%% Define some functions and basic structures
def help_fun():
    """Enters into help page, which prompts user for help for each command.
        All commands are defined in the commandList (list), with their 
        corresponding definitions stored in the commandDict (dictionary)
    """
    list_options()
    
    while True:
        print('\n(Enter <e> to exit to main page)')
        key = input('Which one would you like to see? ')
        key = key.strip()
        if key not in commandList + ['e', 'l', 'h']:
            command_not_found()
        elif key == 'e':
            print('Help page exited. Back to main page.\n')
            break
        elif key == 'l':
            list_options()
        elif key == 'h':
            print('(Showing page for <H>: )')
            key = key.upper()
            print('\nHelp for command: %s' % key)
            print(commandDict[key])
        else:
            print('\nHelp for command: %s' % key)
            print(commandDict[key])
        
def exit_fun():
    print('Exiting program...\n')
    print('Bye!\n\n')
    sys.exit()
    
def command_not_found():
    print('Command not found. Please try again.\n')
    print('(Enter <H/h> to see Help)\n')
    
def list_options():
    print('These are your options:')
    print(commandList)
    print('(Use <l> to see this list again.)')
    
def display_path(path):
    print('This database is based on the csv file: \n')
    print('    ' + path + '\n')
    
def just_print(list1):
    """prints all elements in list1 in a for loop"""
    for stuff in list1:
        print(stuff)
    
def composite_print(list1, list2):
    """Prints in the format of "list1[i] :list2[i]" in a for loop""" 
    for i in range(len(list1)):
        print (list1[i] + ": " + list2[i])

# List of all commands:
commandList = ['H','E','S', 
               'Last','First','Name','Color','Food','Field','Idol']
commandDict = {'H': 'Help page for all commands',
               'E': 'Exit program',
               'S': 'See path of the csv file',
               'Last'   : 'Displays last names of all members',
               'First'  : 'Displays first names of all members',
               'Name'   : 'Displays full names of all members',
               'Color'  : 'Displays the favorite color of each member',
               'Food'   : 'Displays the favorite food of each member', 
               'Field'  : 'Displays the favorite physics field of each member',
               'Idol'   : 'Displays the favorite physicist of each member'
               }

commandList_upper = []      # All user commands converted to UPPER internally
for entry in commandList:
    commandList_upper.append(entry.upper())

#%% Load csv source file and set up dataBase

import sys, csv
import numpy as np

print()

if len(commandDict) != len(commandList):
    print('Commands size mismatch. Program aborted.\n', file=sys.stderr)
    sys.exit()
    
# Load csv files:
csvPATH = '/home/pi/Documents/phys129/yang_homework/yang_hw4/p2_hw4.csv'
csvFile = open(csvPATH)         # create a file object 
csvreader = csv.reader(csvFile) # create a csv reader object

# Assumes no header in csv:
list_of_keys = ['LAST', 'FIRST', 'COLOR', 'FOOD', 'FIELD', 'IDOL'] 

file = []
for row in csvreader:
    # capitalize last name
    last = row[0].title()
    first = row[1].title()
    idol = row[-1].title()
    
    # lower case rest of the entries:
    rest = ','.join(row[2:-1])  # create one string for the rest entries
    rest = rest.lower()         # make all letters lower case
    rest = rest.split(',')      # split back to a list
    
    file.append([last] + [first] + rest + [idol])                  
    
file.sort()                     # sort based on last name, i.e. first entry

# Formatting for easier entry into dictionary
fileArr = np.array(file)        # to use transpose method
fileArr = fileArr.transpose()   # each row corresponds to a key

# Create the dataBase dictionary
dataBase = {}
for i in range(len(list_of_keys)):
    dataBase[list_of_keys[i]] = list(fileArr[i])
    
# Add the option for full names in dataBase:
last = dataBase['LAST']
name = dataBase['FIRST']
for i in range(len(name)):
    name[i] = name[i] + ' ' + last[i]
dataBase['NAME'] = name
    
#%% User Interactive Part

print('Welcome to the Database of p2_hw4!')

print('(Enter <H/h> to see help)')

while True:
    command = input('\nEnter a command: ')
    command = command.upper()           # Convert input to UPPER
    command = command.strip()           # Remove leading and trailing space
    
    if command not in commandList_upper:
        command_not_found()
    
    elif command == 'H':
        help_fun()
        
    elif command == 'E':
        exit_fun()
        
    elif command == 'S':
        display_path(csvPATH)
        
    elif command in commandList_upper[3:6]:   # Only lists the names
        if command == 'NAME':
            print('(Note: sorted by last names):')
            just_print(dataBase[command])

        else:
            just_print(dataBase[command])
    
    elif command in commandList_upper[6:10]:                               # Lists the names, and requested info
        composite_print(dataBase['NAME'], dataBase[command])
