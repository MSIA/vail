# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
from IPython.display import display
from IPython.display import Image
#import glob

path = "T:\courses\MSiA400\Jobs"
#allFiles = glob.glob(path+"\*.csv")


#newjobs = pd.read_csv(path+'20140211_new'+'.csv',header= 0 )

descripjobs = pd.read_csv("file:///T:/courses/MSiA400/Jobs/20140212_descriptions.csv",names = ['JVGUID','Description'], encoding = "ISO-8859-1")
columns = ['JVGUID','DateNew','BUID','CompanyName','Title','OnetCode','Location','Link','a','b','c','d']		
newjobs = pd.read_csv("file:///T:/courses/MSiA400/Jobs/20140212_new.csv", names = columns,encoding = "ISO-8859-1" )
newjobs = newjobs[1:]

combined = pd.merge(descripjobs, newjobs, on='JVGUID', how='outer')



'''
frame = pd.DataFrame()
list_ = []
for file_ in allFiles:
    df = pd.read_csv(file_,index_col=None, header=0)
    list_.append(df)
frame = pd.concat(list_)
''' 
#\20140211_new.csv"
