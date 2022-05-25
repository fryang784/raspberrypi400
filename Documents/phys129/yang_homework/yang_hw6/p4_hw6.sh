#!/bin/sh

#
# p4_hw6.sh - Prints out when Physics 129 webpage announcements last updated
#
# 06May22 Written by Richard Yang
# 

URL='http://web.physics.ucsb.edu/~phys129/lipman/'

echo -n "Latest update time: "
wget -qO - $URL | grep Latest | sed -e 's/^.*">//' -e 's/<.*$//' -e 's/&nbsp;/ /'

# Need to explain the text formating in sed command. 
# The 3rd -e pattern means "substitute all patterns with '&nbsp;' with nothing. 
