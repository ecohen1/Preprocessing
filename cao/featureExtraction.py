from scipy import stats
import numpy as np
import csv

data = np.genfromtxt('../data/panera2windows.csv', delimiter=',')

SWALLOWLABEL = 4
NOTSWALLOWLABEL = 1
SWALLOWOUTPUT = 1
NOTSWALLOWOUTPUT = 0

windowIndex = 0
band1 = []
band2 = []
audio = []
output = []

filename = 'data/panera2features.csv'
with open(filename, 'wb') as csvfile:
    writer = csv.writer(csvfile)

    for index,row in enumerate(data):
        # print index

        if int(row[5]) is windowIndex:
            band1.append(row[0])
            band2.append(row[1])
            audio.append(row[2])
            output.append(row[4])

        else:
            dataClasses = [band1,band2,audio]
            features = []
            statsFunctions = [ np.mean, np.median, max, min, stats.skew, stats.kurtosis, stats.tstd ]
            if len(dataClasses[0]) > 0 and len(dataClasses[1]) > 0 and len(dataClasses[2]) > 0:
                for windowData in dataClasses:
                    for function in statsFunctions:
                        features.append(function(windowData))

                    q25, q75 = np.percentile(windowData, [25,75])
                    features.append(q25)
                    features.append(q75)
                    features.append(q75-q25)

                if np.mean(output) > (SWALLOWLABEL - NOTSWALLOWLABEL)/2.0:
                    features.append(SWALLOWOUTPUT)
                else:
                    features.append(NOTSWALLOWOUTPUT)

                writer.writerow(features)

            windowIndex += 1
            band1 = []
            band2 = []
            audio = []
            output = []
