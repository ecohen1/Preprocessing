# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("C:/Users/Joel/Desktop/necklaceData/deltas.csv")

lst = [df.time[i] - df.time[i-1] for i in range(len(df.time)) if i > 0 and df.time[i] - df.time[i-1] ]
lst.insert(0,0)

df['deltas'] = lst
print sum(lst)/len(lst)
df['deltas'].plot()
counts = df['deltas'].value_counts()
counts.to_csv('C:/Users/Joel/Desktop/necklaceData/counts.csv')

#counts.hist(bins=20)
#plt.hist(counts)
#plt.ylabel('delta T')
#plt.show()

