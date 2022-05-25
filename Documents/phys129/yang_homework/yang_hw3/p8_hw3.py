#!/usr/bin/env python3

#
# p8_hw3.py - Read a csv, print out a statement with each entry
#
# 14Apr22   Richard Yang
#

#
# Problem description:
# 8. Valentine’s Day. 
# Gradeschool students are often required to produce Valentine’s Day cards for  
# each of their classmates, even the ones they don’t like. This repetitive, 
# soulless task is a perfect candidate for computer automation. Use the file 
# classlist.csv from $HOME/physrpi/coursefiles/ and write a program that
# a. Reads in the class list file.
# b. Prints out messages wishing each student a happy Valentine’s Day. 
#    The messages should be formatted like this:
#       Happy Valentine’s Day, Enrico Fermi!
#    The names must be properly capitalized, with remaining letters in lower 
#    case
#

import csv

csvPath = '/home/pi/physrpi/coursefiles/classlist.csv'
csvFile = open(csvPath)         # create a file object 
csvreader = csv.reader(csvFile) # create a csv reader object

# 
# Since there is no header in this csv file
#

names = []
for row in csvreader:
    name = row[1]+' '+row[0]            # Get the full name as a string
    name = name.split()                 # create a list separated by space
    for i in range(len(name)):
        name[i] = name[i].capitalize()  # capitalize each word
    name = ' '.join(name)               # join each word with a space
    names.append(name)                  
    
for name in names:
    print("Happy Valentine's Day, %s!" % name )
