# -*- coding: utf-8 -*-
"""
Created on Wed Mar 02 15:53:23 2016

@author: Joel
"""

import numpy as np
import pandas as pd

#csv to dataframe
timeDF = pd.read_csv("C:/Users/Joel/Desktop/necklaceData/125ms-test.csv")

index_diff_arr = []

order_dict = {}
sorted_times = sorted(timeDF.values)

for index in range(len(sorted_times)):
    time = sorted_times[index][0]
    order_dict[str(time)] = index
    
for test_time_index in timeDF.index:
    real_time_index = order_dict[str(timeDF.values[test_time_index][0])]
    index_diff = test_time_index - real_time_index
    if index_diff != 0:   
        index_diff_arr.append(abs(index_diff))
    
print index_diff_arr    
    
avg_index_diff = np.average(index_diff_arr)
num_index_diff = len(index_diff_arr)

print "\n"
print num_index_diff,"incorrect indexes at an average of", avg_index_diff/2
print "\n"