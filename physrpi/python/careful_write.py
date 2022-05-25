
def careful_write(outlines, filename):
   """Write a list of strings to a file, if the file doesn't yet exist.

      outlines: a list of the strings to be written
      filename: where the strings will be written
   """
   import os
   import sys
   if os.access(filename, os.F_OK):
      print('\nOutput file already exists: %s\n\n' % filename, file=sys.stderr)
      return

   outfile = open(filename, 'w')
   for i in outlines:
      outfile.write(i)
   outfile.close()

