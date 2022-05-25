#!/usr/bin/env python3

#
# server.py - Serve data from a TCP socket
#
# 17May17  Added call to socket.shutdown()
# 10May16  Everett Lipman
#
USAGE="""
usage: server.py port [file]

       Serve data from specified port.
       Default message is sent if no file is specified.
"""
N_ARGUMENTS = (1,2)

import sys
import os
import socket

###############################################################################

def usage(message = ''):
   sys.stdout = sys.stderr
   if message != '':
      print()
      print(message)
   print(USAGE)

   sys.exit(1)
###############################################################################

def check_arguments():
   """Check command line arguments for proper usage.
   """
   global nargs, progname
   nargs = len(sys.argv) - 1
   progname = os.path.basename(sys.argv[0])
   flag = True
   if nargs != 0 and N_ARGUMENTS[-1] == '*':
      flag = False
   else:
      for i in N_ARGUMENTS:
         if nargs == i:
            flag = False
   if flag:
      usage()
   return(nargs)
###############################################################################

def bind_port(prt):
   """Create socket and bind to port prt.
   """

   host = ''  # bind to all available interfaces
 
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # reuse port
   s.bind((host, prt))
   s.listen(1)
    
   return(s)
###############################################################################

if __name__ == '__main__':
   nargs = check_arguments()

   port = int(sys.argv[1])

   if nargs == 1:
      outdata = b'\n\nHello from the server.py program!\n\n'
   else:
      filename = sys.argv[2]
      with open(filename, 'rb') as datafile:
         outdata = datafile.read()

   thesocket = bind_port(port)

   while True:
      connection, peer = thesocket.accept()
      print()
      print('Sending data to %s...' % repr(peer), end='')
      connection.sendall(outdata) 
      print('Done.\n')
      connection.shutdown(socket.SHUT_RDWR)
      connection.close()
