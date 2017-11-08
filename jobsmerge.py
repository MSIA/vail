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
jobs['ExpiredDate'] = pd.to_datetime(jobs['ExpiredDate'])
jobs['DateNew'] = pd.to_datetime(jobs['DateNew'])
#jobs['PostLength'] = int((jobs['ExpiredDate'] - jobs['DateNew']).days)
jobs['FullTimeDesc'] = jobs.Description.str.contains(r'full.?time',case=False)
jobs['PartTimeDesc'] = jobs.Description.str.contains(r'part.?time',case=False)

jobtitles = ['Manager','Sale','Service','Engineer','Specialist','Assistant','Engineer','Specialist','Assistant','Associate','Tech','Senior','Nurse','Analyst','Representative','Customer','Retail','Account','Consultant','Business','Support','Project','Product','Develop','Manage','Operation','President','Software','Director','Admin','Financ','Clinical','Market','Office','Research']

for jobtitle in jobtitles:
    jobs['Has'+jobtitle] = jobs.Title.str.contains(jobtitle,case = False)

#Getting rid of excessively split anomalies

jobsposting = jobs[jobs.a.isnull()]
jobsposting = jobsposting.drop(['a', 'b','c','d'],axis=1)

#jobsposting.to_csv('jobsposting.csv',index=False,quoting=csv.QUOTE_MINIMAL)