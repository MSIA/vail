# -*- coding: utf-8 -*-



import pandas as pd

from IPython.display import display
from IPython.display import Image
import sys, os
import csv



columns = ['JVGUID','DateNew','BUID','CompanyName','Title',
           'OnetCode','Location','Link','a','b','c','d']		

newjobs= pd.DataFrame()
description = pd.DataFrame()
expired = pd.DataFrame()


#Walks through the folder, and creates three separate dataframes of the three different file types
path = "T:\courses\MSiA400\Jobs"


for root, dirs, files in os.walk(path):       
  for file in files: 
    if file.endswith("new.csv"):              
         paths=os.path.join(root,file)
         tables=pd.read_csv(paths, quotechar='"',names = columns,encoding = "ISO-8859-1" )
         newjobs = newjobs.append(tables.drop([0]),ignore_index=True)
         print(paths)
    elif file.endswith("descriptions.csv"):              
         paths=os.path.join(root,file)
         tables=pd.read_csv(paths, quotechar='"',names = ['JVGUID','Description'],encoding = "ISO-8859-1" )
         description = description.append(tables,ignore_index=True)
         print(paths)     
    elif file.endswith("expired.csv"):              
         paths=os.path.join(root,file)
         tables=pd.read_csv(paths, quotechar='"',names = ['JVGUID','ExpiredDate'],encoding = "ISO-8859-1" )
         expired = expired.append(tables,ignore_index=True)
         print(paths)   


      
#Combines the three different file types into a single file, and splits State and city
         
combined1 = pd.merge(description, newjobs, on='JVGUID', how='outer')
jobs = pd.merge(combined1, expired, on='JVGUID', how = 'left')

jobs['State'] = jobs['Location'].str[:2]
jobs['City'] = jobs['Location'].str[3:]


