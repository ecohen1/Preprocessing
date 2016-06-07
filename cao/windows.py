import numpy as np
import csv

data = np.genfromtxt('data/panera3eatingtimed.csv', delimiter=',')
data = data[1:]

EATING = 1
DRINKING = 2
NOTHING = 3
SWALLOW = 4

maxTimeMilli = 500
halfTimeMilli = maxTimeMilli/2

startRow = 0
halfwayIndex = 0
windowIndex = 0
halfwayIndexFound = False
endFound = False
labels = ['band1','band2','audio','timestamp','output','index']
windows = []

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
        # print time, oldTime, timeDiff, nextTimeDiff, sumTimeDiffs, windowIndex
        oldTime = time
        timeOptions = [sumTimeDiffs, sumTimeDiffs + nextTimeDiff]

        if timeOptions[1] > halfTimeMilli and not halfwayIndexFound:
            halfwayIndex = startRow + packetCount
            halfwayIndexFound = True
            if halfTimeMilli - timeOptions[0] > halfTimeMilli - timeOptions[1]:
                halfwayIndex += 1

        elif timeOptions[1] > maxTimeMilli:
            if maxTimeMilli-timeOptions[0] > maxTimeMilli-timeOptions[1]:
                packetCount += 1

            newWindow = data[startRow:startRow+packetCount]
            newWindowPlusIndex = []
            for newRow in newWindow:
                # print len(newRow), len(np.array([windowIndex]))
                # np.concatenate(newRow, np.array([windowIndex]))
                newList = newRow.tolist() + [windowIndex]
                # print len(newList)
                newWindowPlusIndex.append(newList)
            # newWindow = [ newRow + [windowIndex] for newRow in newWindow ]
            # print len(row), len(newWindowPlusIndex[0])
            windows.extend(newWindowPlusIndex)
            windowIndex += 1
            break

        if index is len(data)-1:
            endFound = True
            break

    data = data[halfwayIndex:]

filename = 'data/panera3windows.csv'

with open(filename, 'wb') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(windows)
