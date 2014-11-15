# Joshua Wyss
# 11/15/14
# Setting up the initial Enviornment.
#   - Taking and checking command line arguments
#   - 
# importing programList.txt

#!/usr/bin/python

import sys #gives command line args
prgmLstFile = open(sys.argv[1], 'r')

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#   Command Line Argument Check
#
#   sys.argv[0] prgm name
#   sys.argv[1] prgm list file
#   sys.argv[2] prgm trace file
#   sys.argv[3] user page size
#   sys.argv[4] page replacement algo (clock, lru, fifo)
#   sys.argv[5] pre/demand paging (1 pre; 0 demand)
#
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

if len(sys.argv) != 6:
    sys.exit('Sorry, but you seem not to have the correct number of arguments.')
if (int(sys.argv[3]) % 2) != 0:
    sys.exit('Page Size must be a number divisible by 2 number.')
if (sys.argv[4] is ('clock' and 'lru' and 'fifo')):
    sys.exit('Argument 3 must be either: clock, lru, or fifo')
if ((int(sys.argv[5]) != 0) and (int(sys.argv[4]) != 1)):
    sys.exit('Argument 4 must be either: 1 or 0')

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#   Calculate and Variables
#
#   numFrames   ->  number of frames in main memory
#   prgmTable   ->  the Table of Program (like TOC)
#   numPrgms    ->  number of programs
#
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

numFrames = (512 / int(sys.argv[3]))
prgmTable = []
numPrgms = 0
prgmSizes = []

for x in prgmLstFile:# count the number of programs
    numPrgms += 1

prgmLstFile.seek(0,0)

for pig in prgmLstFile:# put program sizes in list for later use
    prgmSizes.append(int((pig.split())[1]))

print prgmSizes

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#   Setup Programs' Page Table
#
#   [prgm number, 
#        prgm size, 
#        pg size, 
#        pages needed for this prgm, 
#        pg id's 1-x]
#
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

for x in range(0,numPrgms):# initalize prgmTable
    prgmTable.append([])

for x in range(0,numPrgms):# initalize prgmTable contents
    prgmTable[x].append(x)

for x in range(0,numPrgms):# add the program sizes to the list
    prgmTable[x] = prgmTable[x] + [prgmSizes[x]]

for x in range(0,numPrgms):# add page size to the list
    prgmTable[x].append(int(sys.argv[3]))



print prgmTable