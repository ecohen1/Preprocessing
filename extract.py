def markClass(df,tsd,swlist,time):
   i_df = df.set_index([time])
   i_df['Class'] = 0
   for ts in swlist:
       a = str(ts - pd.Timedelta(seconds=tsd))
       b = str(ts + pd.Timedelta(seconds=tsd))
       i_df['Class'][(i_df.index >= a) & (i_df.index < b)] = 1
   return i_df

# input para: input_data , intervals_of_interest , timeString
def markClassPeriod( df , intervals , time ):
   i_df = df.set_index([time])
   i_df['Class'] = 0
   for ts in intervals:
       a = str(ts[0])
       b = str(ts[1])
       i_df['Class'][(i_df.index >= a) & (i_df.index < b)] = 1
   return i_df

def markMultiClassPeriod(df,swlist,class_value,time,passT):
   if (passT):
       i_df = df.set_index([time])
       i_df['Class'] = 0
   else:
       i_df = df
   for ts in swlist:
       a = str(ts[0])
       b = str(ts[1])
       i_df['Class'][(i_df.index >= a) & (i_df.index < b)] = class_value
   return i_df

# input paras: data_label , window_size , start_time , threshold , timeString
def extractWindows( i_df , winsize , startime , threshold , time ):
   ts = startime
   #print "i_df"
   #last timestamp in given data
   endtime = i_df.index.values[-1]

   featL = ["mean","median","max","min","skew","RMS","kurtosis","qurt1",'quart3','irq','stdev','classLabel']
   headlist = list(i_df.keys())
   '''
   headlist = ['Accx', 'Accy', 'Accz', 'Class']
   ‘''

   header = []
   for key in headlist[:-1]:
       for feat in featL[:-1]:
           one = key + "_" + feat
           header.extend([one])

   header.extend([featL[-1]])

   '''
   header:['Accx_mean', 'Accx_median', 'Accx_max', 'Accx_min', 'Accx_skew', 'Accx_RMS', 'Accx_kurtosis', 'Accx_qurt1', 'Accx_quart3', 'Accx_irq', 'Accx_stdev', 'Accy_mean', 'Accy_median', 'Accy_max', 'Accy_min', 'Accy_skew', 'Accy_RMS', 'Accy_kurtosis', 'Accy_qurt1', 'Accy_quart3', 'Accy_irq', 'Accy_stdev', 'Accz_mean', 'Accz_median', 'Accz_max', 'Accz_min', 'Accz_skew', 'Accz_RMS', 'Accz_kurtosis', 'Accz_qurt1', 'Accz_quart3', 'Accz_irq', 'Accz_stdev', 'classLabel']
   ‘''

   allfeats = []
   allfeats.append(header)



   while(ts < endtime):

       ## Assuming ts is staring point of
       a = str(ts)
       b = str(ts + pd.Timedelta(seconds=winsize))
       w_df = i_df[(i_df.index >= a) & (i_df.index < b)]

       # Rate Window and see threshold set window class (working)
       classLabel = 0
       if w_df.Class.mean() > threshold :
           classLabel = 1

       keylist = list(w_df.keys())
       '''
       # keylist=['Accx', 'Accy', 'Accz', 'Class']
       '''

       features = []
       for key in keylist[:-1]:
           win = w_df[key]
           '''
           win = 'Accx', or 'Accy', or 'Accz'
           '''
           irq = win.quantile(q=0.75) - win.quantile(q=0.25)
           features.extend([float(win.mean())]) #mean
           features.extend([float(win.median())]) #median
           features.extend([float(win.max())]) #max
           features.extend([float(win.min())]) #min
           features.extend([float(win.skew())]) #skew
           features.extend([float(sqrt((win**2).mean()))]) #RMS
           features.extend([float(win.kurt())]) #kurtosis
           features.extend([float(win.quantile(q=0.25))]) #1st quartile
           features.extend([float(win.quantile(q=0.75))]) #3rd quartile
           features.extend([float(irq)])#inter quartile range
           #features.extend([float(win.corr())]) #correlation
           features.extend([float(win.std())])#std dev
           # print w_df

       features.extend([classLabel])
       allfeats.append(features)
       ts = ts + pd.Timedelta(seconds=shift_pctg*winsize)

   return allfeats


def extractFeatures( class_type , input_data , region_size , timeString , points_of_interest , window_size , start_time , threshold , labeled_outfile) :
   # ---------------------------------------------------------------
   #  label points according to s_t, e_t
   # ---------------------------------------------------------------

#    data_label = pd.DataFrame()

#    data_label = markClassPeriod( input_data , points_of_interest , timeString )

   # ----------------------------------------------------------------
   #  extract windows among all data and calc features
   # ----------------------------------------------------------------

   data_labelwin = extractWindows(data_label , window_size , start_time , threshold , timeString)

   featDF = pd.DataFrame(data_labelwin[1:] , columns=data_labelwin[0])
   return featDF
