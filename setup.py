# Joshua Wyss
# 11/15/14



#!/usr/bin/python

import sys # gives command line args
import math # Used for floor()


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
if not(int(sys.argv[3]) != 0 and ((int(sys.argv[3]) & (int(sys.argv[3]) - 1)) == 0)):
    sys.exit('Page Size must be a number divisible by 2 number.')
if (sys.argv[4] is ('clock' and 'lru' and 'fifo')):
    sys.exit('Argument 3 must be either: clock, lru, or fifo')
if ((int(sys.argv[5]) != 0) and (int(sys.argv[5]) != 1)):
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


""" * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
Page Replace Methods

    LRU
    FIFO
    Clock

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
                if int(argPreDem) is 1:# Run Pre Paging
                    prgmCounter += 1
                    temp = x
                    if temp >= int(len(mainMem)):
                        temp = 0
                    mainMem[temp][0] = prgmPgNumber
                    mainMem[temp][1] = prgmNumber
                    mainMem[temp][2] = prgmCounter
                    mainMem[temp][3] = 0
                    mainMem[temp][4] = uniquePgNum+1
                break
    # Final Report
    print "/***************************************************"
    print "Page Size: ", int(argPgSz)
    print "Replacement Algorithm: LRU Based Policy"
    if int(argPreDem) is 0:
        print "Paging Policy: Demand Paging"
    if int(argPreDem) is 1:
        print "Paging Policy: Pre Paging"
    print "Total Page Faults: ", pageFaults
    print "/***************************************************"

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
                if int(argPreDem) is 1:# Run Pre Paging
                    prgmCounter += 1
                    temp = x
                    if temp >= int(len(mainMem)):
                        temp = 0
                    mainMem[temp][0] = prgmPgNumber
                    mainMem[temp][1] = prgmNumber
                    mainMem[temp][2] = prgmCounter
                    mainMem[temp][3] = 0
                    mainMem[temp][4] = uniquePgNum+1
                break
                # Final Report
    print "/***************************************************"
    print "Page Size: ", int(argPgSz)
    print "Replacement Algorithm: FIFO Based Policy"
    if int(argPreDem) is 0:
        print "Paging Policy: Demand Paging"
    if int(argPreDem) is 1:
        print "Paging Policy: Pre Paging"
    print "Total Page Faults: ", pageFaults
    print "/***************************************************"

def clock():
    global prgmCounter
    global pageFaults
    pageFaults = 0
    clockPointer = 0
    for i in prgmTraceFile:
        prgmNumber = int((i.split())[0])
        prgmPgNumber = int(math.floor(float((i.split())[1])/int(argPgSz)))/2
        uniquePgNum = allPrgmTable[prgmNumber][4][prgmPgNumber]
        replaced = 0
        for x in range(0,len(mainMem)):# Found it!
            if uniquePgNum is mainMem[x][4]:
                mainMem[x][2] = prgmCounter
                mainMem[x][3] = 1
                replaced = 1
                break
        #import pdb; pdb.set_trace()
        if replaced is 0:
            for x in range(0,len(mainMem)):# Try Empty Space
                if mainMem[x][0] is None:
                    mainMem[x][0] = prgmPgNumber
                    mainMem[x][1] = prgmNumber
                    mainMem[x][2] = prgmCounter
                    mainMem[x][3] = 1
                    mainMem[x][4] = uniquePgNum
                    pageFaults += 1
                    replaced = 1
                    if int(argPreDem) is 1:# Run Pre Paging
                        prgmCounter += 1
                        temp = x
                        if temp >= int(len(mainMem)):
                            temp = 0
                        mainMem[temp][0] = prgmPgNumber
                        mainMem[temp][1] = prgmNumber
                        mainMem[temp][2] = prgmCounter
                        mainMem[temp][3] = 0
                        mainMem[temp][4] = uniquePgNum+1
                    break
        if replaced is 0:
            for x in range(0,len(mainMem)):# Do the clock swap
                next = 0
                if clockPointer >= ((len(mainMem)) - 1):
                    clockPointer = 0
                if mainMem[clockPointer][3] is 1:
                    mainMem[clockPointer][3] = 0
                    next = 1
                    clockPointer += 1
                if (mainMem[clockPointer][3] is 0) or (next is 0):
                    mainMem[clockPointer][0] = prgmPgNumber
                    mainMem[clockPointer][1] = prgmNumber
                    mainMem[clockPointer][2] = prgmCounter
                    mainMem[clockPointer][3] = 1
                    mainMem[clockPointer][4] = uniquePgNum
                    pageFaults += 1
                    replaced = 1
                    clockPointer += 1
                    if int(argPreDem) is 1:# Run Pre Paging
                        prgmCounter += 1
                        temp = x
                        if temp >= int(len(mainMem)):
                            temp = 0
                        mainMem[temp][0] = prgmPgNumber
                        mainMem[temp][1] = prgmNumber
                        mainMem[temp][2] = prgmCounter
                        mainMem[temp][3] = 0
                        mainMem[temp][4] = uniquePgNum+1
                    break
        prgmCounter += 1
    # Final Report
    print "/***************************************************"
    print "Page Size: ", int(argPgSz)
    print "Replacement Algorithm: Clock Based Policy"
    if int(argPreDem) is 0:
        print "Paging Policy: Demand Paging"
    if int(argPreDem) is 1:
        print "Paging Policy: Pre Paging"
    print "Total Page Faults: ", pageFaults
    print "/***************************************************"

if argReplaceAlgo == "lru":
    lru()
if argReplaceAlgo == "fifo":
    fifo()
if argReplaceAlgo == "clock":
    clock()



