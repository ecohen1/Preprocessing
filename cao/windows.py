'''
This code takes in the output of csv-modifier.py and splits it into 500 millisecond
    windows with 50 percent overlap, writing the output to filename in the same format
        as the input
'''

import numpy as np
import csv

data = np.genfromtxt('data/panera3eatingtimed.csv', delimiter=',')
data = data[1:]

EATING = 1
DRINKING = 2
NOTHING = 3
SWALLOW = 4

maxTimeMilli = 500
percentOverlap = 0.5
newBeginTimeMilli = maxTimeMilli*percentOverlap

startRow = 0
newBeginIndex = 0
windowIndex = 0
newBeginIndexFound = False
endFound = False
labels = ['band1','band2','audio','timestamp','output','index']
windows = []

filename = 'data/panera3windows.csv'

while not endFound and len(data) > 0:

    packetCount = 0
    timeDiff = 0
    sumTimeDiffs = 0
    oldTime = 0
    timeOffset = data[0][3]

    for index, row in enumerate(data):
        packetCount += 1

        time = row[3] - timeOffset
        timeDiff = time - oldTime
        sumTimeDiffs += timeDiff
        if index < len(data)-1:
            nextTime = data[index+1][3] - timeOffset
            nextTimeDiff = nextTime - time
        else:
            nextTimeDiff = maxTimeMilli
        oldTime = time
        timeOptions = [sumTimeDiffs, sumTimeDiffs + nextTimeDiff]

        if timeOptions[1] > newBeginTimeMilli and not newBeginIndexFound:
            newBeginIndex = startRow + packetCount
            newBeginIndexFound = True
            if newBeginTimeMilli - timeOptions[0] > newBeginTimeMilli - timeOptions[1]:
                newBeginIndex += 1

        elif timeOptions[1] > maxTimeMilli:
            if maxTimeMilli-timeOptions[0] > maxTimeMilli-timeOptions[1]:
                packetCount += 1

            newWindow = data[startRow:startRow+packetCount]
            newWindowPlusIndex = []
            for newRow in newWindow:
                newList = newRow.tolist() + [windowIndex]
                newWindowPlusIndex.append(newList)
            windows.extend(newWindowPlusIndex)
            windowIndex += 1
            break

        if index is len(data)-1:
            endFound = True
            break

    data = data[newBeginIndex:]

with open(filename, 'wb') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(windows)
