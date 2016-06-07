'''
This code takes in a csv file with data logged by the phone application (NeckMonitor)
    and filters out any periods that are labeled as nothing (3), writing the result to 'filename'
'''

import numpy as np
import csv

data = np.genfromtxt('data/panera3.csv', delimiter=',')
EATING = 1
SWALLOW = 4

filename = 'data/panera3eatingtimed.csv'

with open(filename, 'wb') as csvfile:
    writer = csv.writer(csvfile)
    labels = ['band1','band2','audio','timestamp','output']
    writer.writerow(labels)
    newdata = [ [row[2],row[3],row[4],row[7],row[8]] for row in data if row[8] in [EATING,SWALLOW]]
    writer.writerows(newdata)
    print filename
