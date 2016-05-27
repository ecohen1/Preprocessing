import numpy as np

data = np.genfromtxt('data/panera3.csv', delimiter=',')

newdata = ([[row[2],row[3],row[4],row[8]] for row in data if row[8] != 3 and row[8] != 2])
newdata[0] = [1,2,3,4]

np.savetxt("data/panera3eating.csv", newdata, delimiter=",")
