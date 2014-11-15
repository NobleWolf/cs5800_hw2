# Joshua Wyss
# 11/15/14
# Setting up the initial Enviornment.
#   - Taking and checking command line arguments
#   - 
# importing programList.txt

#!/usr/bin/python

import sys #gives command line args
prgmlst = open(sys.argv[1], 'r')

# * * * * * * * * * * * * * * * * * * * * * 
#   Command Line Argument Check
# * * * * * * * * * * * * * * * * * * * * * 

if len(sys.argv) != 6:
    sys.exit('Sorry, but you seem not to have the correct number of arguments.')
if (int(sys.argv[3]) % 2) != 0:
    sys.exit('Page Size must be a number divisible by 2 number.')
if (sys.argv[4] is ('clock' and 'lru' and 'fifo')):
    sys.exit('Argument 3 must be either: clock, lru, or fifo')
if ((int(sys.argv[5]) != 0) and (int(sys.argv[4]) != 1)):
    sys.exit('Argument 4 must be either: 1 or 0')

# * * * * * * * * * * * * * * * * * * * * * 
#   Next Section
# * * * * * * * * * * * * * * * * * * * * * 