#!/usr/bin/env python3

#
# iminuit_test.py - Simple test of iminuit library
#
# 19Feb20  Transcribed by EL from https://code.activestate.com/pypm/iminuit/
#

from iminuit import Minuit

def f(x,y,z):
   return (x-2)**2 + (y-3)**2 + (z-4)**2

m = Minuit(f)
m.migrad()

print(m.values)  #{'x':2,'y':3,'z':4}
print( m.errors)
