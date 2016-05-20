# -*- coding: utf-8 -*-
"""
Created on Wed Mar 02 15:53:23 2016

@author: Joel
"""

# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import math

#csv to dataframe
trueDF = pd.read_csv("C:/Users/Joel/Desktop/necklaceData/25ms-long.csv")
testDF = pd.read_csv("C:/Users/Joel/Desktop/necklaceData/25ms-long-test.csv")

true_length = len(trueDF.index)
num_missed = 0
true_index = 0
missed_arr = []
wrong_val_arr = []
wrong_val_index_arr = []
diff_arr = []

for index in testDF.index:
    if index < true_length:
        #skip the missed rows in the true table until getting matching rows
        #NOTE: IF VALUES GET SWITCHED IN TRANSIT, while looop doesnt fire
        #print trueDF.values[true_index][0]
        #print testDF.values[index][0]
        while trueDF.values[true_index][0] < testDF.values[index][0]:
            missed_arr.append(trueDF.values[true_index])
            true_index += 1
            
        #compare the data in the matching rows
        for i in range(1):
            data = testDF.values[index][i]
            true_data = trueDF.values[true_index][i]
            if data != true_data:
                wrong_val_arr.append(data)
                wrong_val_index_arr.append(i)
                diff_arr.append(abs(data-true_data))
        true_index += 1

if trueDF.values[-1][0] > testDF.values[-1][0]:
    num_missed = len(missed_arr) + (trueDF.values[-1][0] - testDF.values[-1][0])
else:
    num_missed = len(missed_arr)
    
num_wrong = len(wrong_val_arr)
avg_wrong = np.average(wrong_val_arr)
avg_diff = np.average(diff_arr)
if math.isnan(avg_diff):
    avg_diff = 0
        
print "missed", num_missed, "out of", len(trueDF.index)
print num_wrong, "wrong values at an avg of", avg_wrong
if num_wrong > 0:
    print "the average amount off was", avg_diff
    for j in range(1,6):
        print wrong_val_index_arr.count(j), "values wrong in column", j+1
