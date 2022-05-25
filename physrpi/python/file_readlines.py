
def file_readlines(filename):
   """Read text file and return the contents as a list of lines.
   """
   infile = open(filename, 'r')
   inlines = infile.readlines()
   infile.close()
   return(inlines)

