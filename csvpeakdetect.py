import peakdetect as pd
from numpy import genfromtxt
import matplotlib.pyplot as plt

data = genfromtxt('moving-average-results.csv', delimiter=',')

avgdata = [data[i][0] for i in range(len(data))]
labeldata = [data[i][4]*.75 for i in range(len(data))]
indices = [i for i in range(len(data))]
# print avgdata
# print labeldata

plt.plot(indices, labeldata, 'g')
plt.plot(indices, avgdata,'r')

peaks = pd.peakdetect(avgdata, lookahead=25)
peakvals = [peaks[i] for i in range(len(peaks))]
peakvalsx = [val[0] for val in peakvals[0]]
peakvalsy = [val[1] for val in peakvals[0]]
# print peakvals

plt.scatter(peakvalsx,peakvalsy)
plt.show()
