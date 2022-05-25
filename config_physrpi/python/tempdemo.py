#!/usr/bin/env python3
#
# tempdemo.py - Temperature measurement demo with MCP9808
#
# 09May22  Converted code to use Adafruit Blinka and CircuitPython
# 18May16  Adapted from Adafruit code by Everett Lipman
#

import time
import board
import busio
import adafruit_mcp9808
##############################################################################

def cel2far(T):
   """Convert T from Celsius to Fahrenheit
   """
   return(1.8*T + 32.0)
##############################################################################

#
# Default address is 0x18
#
# alternative: mcp = adafruit_mcp9808.MCP9808(i2c, address=0x19)
#

with board.I2C() as i2c:
   sensor = adafruit_mcp9808.MCP9808(i2c)

   while True:
      Tc = sensor.temperature  # float
      Tf = cel2far(Tc)
      print('%.4f degC  %.4f degF' % (Tc, Tf))
      time.sleep(0.5)
