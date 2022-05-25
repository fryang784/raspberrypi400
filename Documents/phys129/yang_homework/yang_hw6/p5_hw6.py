#!/usr/bin/env python3

#
# p5_hw6.py - Get web page with socket
# 06May22  Richard Yang 
#
# Problem Description:
# 5. Get Web Page with socket. 
# Write a Python program that prints out for the user when the Physics 129 web 
# page announcements were last updated. Retrieve the course web page by opening 
# a raw socket to port 80 on the server.
# Hints: See the client.py example.
# Before reading the data, you must send an http command through the socket. It
# will look similar to this: b’GET / HTTP/1.0\r\n\r\n’
# 
USAGE="""
usage: p5_hw6.py

       Print latest update time for phys129 web page.
       Web page connection established and data retrieved using socket.
"""

ipnum = '128.111.17.41'         # web.physics.ucsb.edu
port = 80                       # http port
req = b'GET /~phys129/lipman/ HTTP/1.0\r\n\r\n' # get phys129 web page
term = 'Latest update'

import socket
import sys

#%%============================================================================
# Define functions
#==============================================================================
def usage(message = ''):
    sys.stdout = sys.stderr
    if message != '':
        print()
        print(message)
    print(USAGE)

    sys.exit(1)

def open_connection(ipn, prt):
    """Open TCP connectin to ipnum:port.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    connect_error = s.connect_ex((ipn, prt))

    if connect_error:
        if connect_error == 111:
            usage('Connection refused.  Check address and try again.')
        else:
            usage('Error %d connecting to %s:%d' % (connect_error,ipn,prt))

    return(s)
###############################################################################

def receive_data(thesock, nbytes):
    """Attempt to receive nbytes of data from open socket thesock.
    """
    dstring = b''
    rcount = 0  # number of bytes received
    thesock.settimeout(5)
    while rcount < nbytes:
        try:
            somebytes = thesock.recv(min(nbytes - rcount, 2048))
        except socket.timeout:
            # print('Connection timed out.', file = sys.stderr)
            break
        if somebytes == b'':
            # print('Connection closed.', file = sys.stderr)
            break
        rcount = rcount + len(somebytes)
        dstring = dstring + somebytes

    # print('\n%d bytes received.\n' % rcount)

    return(dstring)
#%%============================================================================
# Script
#==============================================================================

# print()
# print('Connecting to %s, port %d...\n' % (ipnum, port))

thesocket = open_connection(ipnum, port)

# Send http command to get phys129 web page
thesocket.sendall(req)

# Receive response from web server
indata = receive_data(thesocket, 4096)
thesocket.shutdown(socket.SHUT_RDWR)
thesocket.close()

datastring = indata.decode()        # convert from bytestring to string

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
