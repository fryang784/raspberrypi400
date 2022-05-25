#!/usr/bin/env python3

# 
# p7_hw6.py - Get web page with requests
# 06May22  Richard Yang
#
# Problem Description:
# 7. Time Server. 
# Write a program that serves the current time in human-readable format when a 
# connection is established to TCP port 55555 on your RPi.
# Hints: See the server.py example.
# Start the Python interpreter, then type:
# import time
# help(time)
# Use the space bar and ’b’ to page forward and back.
#
USAGE="""
usage: p7_hw6.py 

       Serve the current time from specified port.
"""

port = 55555                    # bind to specified port number

import socket
import time
#%%============================================================================
# Define functions
#==============================================================================

def bind_port(prt):
   """Create socket and bind to port prt.
   """

   host = ''  # bind to all available interfaces
 
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # reuse port
   s.bind((host, prt))
   s.listen(1)
    
   return(s)

#%%============================================================================
# Script
#==============================================================================
tstring = time.asctime()
outdata = bytes(tstring, 'ascii') 

thesocket = bind_port(port)

while True:
    connection, peer = thesocket.accept()
    print()
    print('Sending data to %s...' % repr(peer), end='')
    connection.sendall(outdata) 
    print('Done.\n')
    connection.shutdown(socket.SHUT_RDWR)
    connection.close()
