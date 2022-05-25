#!/usr/bin/env python3

#
# p6_hw5.py - User input petal ps script output
# 29Apr22   Richard Yang, 
#
# Problem Description:
# 6. PostScript Flower. Examine the code in $HOME/physrpi/ps/petal.ps on your 
# RPi, and use the gv program to view the result. Write a program in Python 
# that takes as input from the user a number of petals, then writes to disk a 
# PostScript program (a .ps file) that draws a flower with the specified number
# of non-overlapping, symmetrically placed petals. Your program may limit the 
# number of petals to some reasonable range.
# Extra credit will be given for a stem and leaves.
# Hints: Remember you can use triple quotes to create multiple-line strings. 
# Assemble your output as one large string, then use the appropriate file 
# method to write it to disk. You can concatenate strings with +. I suggest 
# you not try to write elegant PostScript code. Do all the work (for example, 
# loops and calculations) in Python, and make the PostScript output as simple 
# as possible.

# 
# See petal.ps
#

import sys, os
import numpy as np
from datetime import date

x = 55                              # for cp1 = [ 55 65 ]
y = 65

theta0 = np.arctan(x/y) * 180/np.pi # degrees, from vertical axis

xscale = 1                          
yscale = 1

translate = (306, 500)              # translate to this coordinate

date = date.today()
d1 = date.strftime("%d%b%y")

def careful_print(fname, string):
    """Similar to careful_write, but takes in a long string, instead of a list 
       of strings.
    """
    if os.access(fname, os.F_OK):
        print('\nOutput file already exists: %s\n' % fname, file=sys.stderr)
        print('script not saved.\n\n')
    else: 
        outfile = open(fname, 'w')
        outfile.write(string)
        outfile.close()

def Header(Num):
    return"%!PS\n%\n% p6_hw5_petal.ps - " + \
        str("Draw flower with %d petals\n"% Num)+"%\n% " + d1 + \
        """  Richard Yang\n%\n\n%\n% draw petal scaled by xscale and yscale, 
% rotated by angle.\n%\n"""

Prolog="""/petal  % xscale yscale angle petal
   {
   /petalcol [ 0.8 0 0 ] def
   /ep1 [ 0 0 ] def
   /ep2 [ 0 100 ] def
   /cp1 [ 55 65 ] def
   /cp2 [ 10 95 ] def
   /ap {aload pop} def
   gsave
   petalcol ap setrgbcolor
   0 setlinewidth
   rotate  % use angle from stack
   scale   % use xscale and yscale from stack

   ep1 ap moveto
   cp1 ap cp2 ap ep2 ap curveto
   cp2 ap exch neg exch
   cp1 ap exch neg exch
   ep1 ap curveto closepath fill
   
   grestore
   } def
   
/stem % stem
   {
   /stemcol [ 0 0.8 0] def
   /ep1 [ 0 0 ] def
   /ep2 [ 0 -300] def
   /ep3 [ 10 -300] def
   /cp1 [ -30 -100] def
   /cp2 [ -20 -200] def
   /ap {aload pop} def
   gsave
   stemcol ap setrgbcolor
   0 setlinewidth

   ep1 ap moveto
   cp1 ap cp2 ap ep2 ap curveto
   ep3 ap lineto
   cp2 ap cp1 ap ep1 ap curveto closepath fill

   grestore
   } def

"""

def draw_gfun(Num, theta_arr):
    global xscale
    global yscale
    string = "gsave\n"+str("   %d %d translate\n\n" %translate)
    
    string+="   stem\n"
    
    for i in range(Num):
        string+=str("   %.3f %.3f %.3f petal\n"%(xscale,yscale,theta_arr[i]))
        
    string+="grestore\n\nshowpage"
    
    return string
       
    

#%%
print()

Num = input('Enter the number of petals: ')

Num = Num.strip()

try:
    Num = int(Num)
except ValueError:
    print('Input must be a non-zero integer.', file=sys.stderr)
else: 
    if Num < 1:
        print('Input must be a non-zero integer.', file=sys.stderr)
        exit(1)

theta_arr = np.linspace(0,360,Num+1)        # last element back to 360
theta_arr = theta_arr[:-1]                  # last element redundant

theta = theta_arr[1]                        # the angle interval

if theta0*2 > theta:
    
    # Use theta to redefine a scaled position of cp1
    # This only changes xscale
    x_shrink = np.tan(theta/2 * np.pi/180) * y
    xscale = x_shrink/x
    print('xscale=%.3f' %xscale)
else:
    print('ok')
    pass


script = Header(Num)+Prolog+draw_gfun(Num,theta_arr)
print()
# print(script)


fname = str('p6_hw5_petal%d_'%Num)+d1+'.ps'

careful_print(fname, script)