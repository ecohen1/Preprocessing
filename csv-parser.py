# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import math

#csv to dataframe
trueDF = pd.read_csv("C:/Users/Joel/Desktop/data.csv")
testDF = pd.read_csv("C:/Users/Joel/Desktop/data2.csv")

num_missed = 0
true_index = 0
missed_arr = []
wrong_val_arr = []
diff_arr = []

for index in testDF.index:
    #skip the missed rows in the true table until getting matching rows
    while trueDF.values[true_index][0] < testDF.values[index][0]:
        missed_arr.append(trueDF.values[true_index])
        true_index += 1
        
    #compare the data in the matching rows
    for i in range(1,6):
        data = testDF.values[index][i]
        true_data = trueDF.values[true_index][i]
        if data != true_data:
            wrong_val_arr.append(data)
            diff_arr.append(abs(data-true_data))
    true_index += 1

num_missed = len(missed_arr) + (trueDF.values[-1][0] - testDF.values[-1][0])
num_wrong = len(wrong_val_arr)
avg_wrong = np.average(wrong_val_arr)
avg_diff = np.average(diff_arr)
if math.isnan(avg_diff):
    avg_diff = 0
        
print "missed", num_missed, "out of", len(trueDF.index)
print num_wrong, "wrong values at an avg of", avg_wrong
print "the average amount off was", avg_diff