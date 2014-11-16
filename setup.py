# Joshua Wyss
# 11/15/14
# Setting up the initial Enviornment.
#   - Taking and checking command line arguments
#   - 
# importing programList.txt

#!/usr/bin/python

import sys # gives command line args
import math


""" * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
Command Line Argument Check

    sys.argv[0] prgm name
    sys.argv[1] prgm list file
    sys.argv[2] prgm trace file
    sys.argv[3] user page size
    sys.argv[4] page replacement algo (clock, lru, fifo)
    sys.argv[5] pre/demand paging (1 pre; 0 demand)

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"""

if len(sys.argv) != 6:
    sys.exit('Sorry, but you seem not to have the correct number of arguments.')
if (int(sys.argv[3]) % 2) != 0:
    sys.exit('Page Size must be a number divisible by 2 number.')
if (sys.argv[4] is ('clock' and 'lru' and 'fifo')):
    sys.exit('Argument 3 must be either: clock, lru, or fifo')
if ((int(sys.argv[5]) != 0) and (int(sys.argv[4]) != 1)):
    sys.exit('Argument 4 must be either: 1 or 0')

argPgSz = sys.argv[3]
argReplaceAlgo = sys.argv[4]
argPreDem = sys.argv[5]


prgmLstFile = open(sys.argv[1], 'r')
prgmTraceFile = open(sys.argv[2], 'r')

""" * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
Calculate and Variables

    numFrames       ->  number of frames in main memory
    allPrgmTable    ->  the Table of Program (like TOC)
    numPrgms        ->  number of programs
    mainMem         ->  The Main Memory, made up of frames
    prgmCounter     ->  Global program counter
    pageFaults      ->  Duh...

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"""

mainMemSz = 512
numFrames = int(math.floor(round(float(mainMemSz)/int(argPgSz))))
allPrgmTable = []
numPrgms = 0
prgmSizes = []
mainMem = []
prgmCounter = 0
tracePrgmNum = []
traceRelWordNum = []
pageFaults = 0

for x in prgmLstFile:# count the number of programs
    numPrgms += 1

prgmLstFile.seek(0,0)# be kind please rewind

for pig in prgmLstFile:# put program sizes in list for later use
    prgmSizes.append(int((pig.split())[1]))

prgmLstFile.seek(0,0)

for pig in prgmTraceFile:
    tracePrgmNum.append(int((pig.split())[0]))
    traceRelWordNum.append(int((pig.split())[1]))

prgmTraceFile.seek(0,0)# be kind please rewind

""" * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
Setup Programs' Page Table

    [prgm number, 
     prgm size, 
     pg size, 
     pages needed for this prgm, 
     pg id's 1-x]

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"""

for x in range(0,numPrgms):# initalize allPrgmTable
    allPrgmTable.append([])

tempidhold = 0

# initalize allPrgmTable contents
for x in range(0,numPrgms):
    allPrgmTable[x].append(x)# prgm numbers
    allPrgmTable[x] = allPrgmTable[x] + [prgmSizes[x]]# add the program sizes to the list
    allPrgmTable[x].append(int(argPgSz))# add page size to the list
    allPrgmTable[x].append(int(round(float(prgmSizes[x])/int(argPgSz))))# Pages needed for program x **> Should I have minus 1? <**
    temp = tempidhold + int(round(float(prgmSizes[x])/int(argPgSz))) - 1
    allPrgmTable[x].append(range(tempidhold,temp))
    tempidhold = temp

""" * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
Setup Memory Frames

    initPages   ->  Initial page allocation for each program

    Main Memory has:
    -Page Number
    -prgmNum
    -Time
    -use bit; no > 0, yes > 1
    -Unique Number

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * """

initPages = int(math.floor(round(float(numFrames)/int(numPrgms))))-1# number of pages allocated to each program on init.

for x in range(0,numFrames):# Init main memory
    mainMem.append([])

# >>> Initializing Main Memory Values
for x in range(0,numPrgms):# x is prgm number
    for y in range(0, initPages):# y is Page Number for program x
        mainMem[prgmCounter].append(y)# Page Number
        mainMem[prgmCounter].append(x)# Program Number
        mainMem[prgmCounter].append(prgmCounter)# time added
        mainMem[prgmCounter].append(0)# Use Bit
        mainMem[prgmCounter].append((allPrgmTable[x][4][y]))
        prgmCounter += 1  
        if (y is allPrgmTable[x][3]):# if the program size is smaller than can fit in given space
            for z in range(y,initPages):
                mainMem[prgmCounter].append(None)# none because it has run out of pages to add for this program
                mainMem[prgmCounter].append(x)
                mainMem[prgmCounter].append(prgmCounter)
                mainMem[prgmCounter].append(0)
                mainMem[prgmCounter].append(None)
                prgmCounter += 1
            break
if (not(len(mainMem) < prgmCounter)):
    for x in range(prgmCounter,len(mainMem)):
        mainMem[prgmCounter].append(None)# none because it has run out of pages to add for this program
        mainMem[prgmCounter].append(None)
        mainMem[prgmCounter].append(prgmCounter)
        mainMem[prgmCounter].append(0)
        mainMem[prgmCounter].append(None)
        prgmCounter += 1

# print mainMem



""" * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
Page Replace Methods

    LRU

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * """

def lru():
    global prgmCounter
    global pageFaults
    pageFaults = 0
    for i in prgmTraceFile:
        prgmNumber = int((i.split())[0])
        prgmPgNumber = int(math.floor(float((i.split())[1])/int(argPgSz)))/2
        uniquePgNum = allPrgmTable[prgmNumber][4][prgmPgNumber]

        oldestEntry = int(min(mainMem, key=lambda L: L[2])[2])
        prgmCounter += 1
        for x in range(0,len(mainMem)):
            if mainMem[x][4] is uniquePgNum:
                mainMem[x][2] = prgmCounter
                mainMem[x][3] = 1
                break
            if mainMem[x][2] == oldestEntry:
                mainMem[x][0] = prgmPgNumber
                mainMem[x][1] = prgmNumber
                mainMem[x][2] = prgmCounter
                mainMem[x][3] = 0
                mainMem[x][4] = uniquePgNum
                pageFaults += 1
                break

def fifo():
    global prgmCounter
    global pageFaults
    pageFaults = 0
    for i in prgmTraceFile:
        prgmNumber = int((i.split())[0])
        prgmPgNumber = int(math.floor(float((i.split())[1])/int(argPgSz)))/2
        uniquePgNum = allPrgmTable[prgmNumber][4][prgmPgNumber]

        oldestEntry = int(min(mainMem, key=lambda L: L[2])[2])
        prgmCounter += 1
        for x in range(0,len(mainMem)):
            if mainMem[x][4] is uniquePgNum:
                mainMem[x][3] = 1
                break
            if mainMem[x][2] == oldestEntry:
                mainMem[x][0] = prgmPgNumber
                mainMem[x][1] = prgmNumber
                mainMem[x][2] = prgmCounter
                mainMem[x][3] = 0
                mainMem[x][4] = uniquePgNum
                pageFaults += 1
                break

def clock():
    global prgmCounter
    global pageFaults
    pageFaults = 0
    for i in prgmTraceFile:
        prgmNumber = int((i.split())[0])
        prgmPgNumber = int(math.floor(float((i.split())[1])/int(argPgSz)))/2
        uniquePgNum = allPrgmTable[prgmNumber][4][prgmPgNumber]
        clockPointer = 0

        prgmCounter += 1
        for x in range(0,len(mainMem)):
            
            if x is len(mainMem):# both fail!
                pageFaults += 1
                for z in range(0,len(mainMem)):
                    y = z+clockPointer
                    if y > len(mainMem):
                        y = 0
                    if mainMem[z][3] is 0:
                        mainMem[z][0] = prgmPgNumber
                        mainMem[z][1] = prgmNumber
                        mainMem[z][2] = prgmCounter
                        mainMem[z][3] = 1
                        mainMem[z][4] = uniquePgNum
                        break
                    if mainMem[z][3] is 1:
                        mainMem[z][3] = 0
                break
            if mainMem[x][4] is None:# is there any empty space?
                mainMem[x][0] = prgmPgNumber
                mainMem[x][1] = prgmNumber
                mainMem[x][2] = prgmCounter
                mainMem[x][3] = 1
                mainMem[x][4] = uniquePgNum
                pageFaults += 1
                break
            if mainMem[x][4] is uniquePgNum:# is it already in there?
                mainMem[x][2] = prgmCounter
                mainMem[x][3] = 1
                break




# lru()
# fifo()
clock()
print mainMem
print pageFaults

# import pdb; pdb.set_trace()



