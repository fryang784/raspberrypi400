#!/usr/bin/python3

#
# subproc_ls.py - Demonstrate subprocess module by running ls
#
# See https://docs.python.org/3.4/library/subprocess.html
#
# 27Apr17  Added missing "-" to "-al" option in command line list 
# 13Apr16  Changed examples and added comments
# 11Apr16  Written by Everett Lipman
#

import subprocess

print()

#
# Simple call to ls with no arguments. Returns exit status (an integer).
# 0 indicates no error.
# Standard output from subprocess.call() goes to the screen.
#
print("subprocess.call('ls'):\n")
ret = subprocess.call('ls')

print("ls returned exit status %d." % ret)
print('----------------------------------------------------------------------')
print()

#
# Call to ls with options '-al foobar.txt'.
# Here I assume foobar.txt does not exist, so exit status
# will be nonzero, indicating an error.
#
# ['ls', '-al', 'foobar.txt'] is a list of strings.
#
print("subprocess.call(['ls','-al','foobar.txt']):\n")
ret = subprocess.call(['ls','-al','foobar.txt'])

print("ls -al foobar.txt returned exit status %d." % ret)
print('----------------------------------------------------------------------')
print()

#
# Here I use subprocess.check_output(), which returns the standard output
# rather than the exit status.  It will raise an exception and stop
# the program if there is an error.
#
# universal_newlines=True tells Python that we are expecting plain
# text output from the ls command.
#
print("subprocess.check_output('ls', universal_newlines=True)\n")
output_text = subprocess.check_output('ls', universal_newlines=True)

print("The output of 'ls' was:")
print()
print(output_text)
print('----------------------------------------------------------------------')
print()

#
# Force column output with ls -C
#
print("subprocess.check_output(['ls','-C'], universal_newlines=True)\n")

output_text = subprocess.check_output(['ls','-C'], universal_newlines=True)
print("The output of 'ls -C' was:")
print()
print(output_text)
print()
