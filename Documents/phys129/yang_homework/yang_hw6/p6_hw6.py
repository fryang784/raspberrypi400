#!/usr/bin/env python3

# 
# p6_hw6.py - Get web page with requests
# 06May22  Richard Yang
#
# Problem Description:
# 6. Get Web Page with Requests. 
# Write a Python program that prints out for the user when the Physics 129 web 
# page announcements were last updated. Retrieve the course web page using 
# requests, and process the result using either string methods or bs4.
# Hints:
# If you decide to use bs4, you may need to import re and use a BeautifulSoup 
# method to search for text = re.compile(’RE’), where ’RE’ is a regular 
# expression that matches the text you want to find.
# https://requests.readthedocs.io/en/master/
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#searching-the-tree
#
USAGE="""
usage: p6_hw6.py

       Print latest update time for phys129 web page.
       Web page data retrieved using requests.
"""

URL = 'http://web.physics.ucsb.edu/~phys129/lipman/'
term = 'Latest update'

import requests
import sys

#%%============================================================================
# Script
#==============================================================================

r = requests.get(URL)

datastring = r.text

# Split the string into a rows
datalist = datastring.split('\n')

# Get the row containing the term 
for i in range(len(datalist)):
    if term in datalist[i]:
        row = datalist[i]
        break

#
# The time comes after the first occurance of '>', and THEN a '<'
#

# truncate everything before first occurance of '>'
row = row.split('>')[1]

# truncate everything after '<'
row = row.split('<')[0]

# Replace the html character for space if necessary
if '&nbsp;' in row:
    row = row.replace('&nbsp;', ' ')

print('Latest update time: %s' %row)
