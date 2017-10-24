"""
Vail Project - Job Ads Data Cleaning
"""

import pandas as pd
from glob import iglob


# Combining on all text files
for pathname in iglob('T:\courses\MSiA400\Jobs\ex*log'):
    
    # Read each data file
    with open(pathname, 'r') as f:
        file = f.readlines()
        fields = file[3].split()[1:]
        data = file[4:]
        
        for i, row in enumerate(data):
            l = row.split()
            data[i] = l
        
        # Create data frame
        df = pd.DataFrame(data, columns = fields)
        df['file'] = pathname[24:]
        
        # Append to user data
        user_data = df[(df['time-taken'].str.isnumeric() == True)]
        user_data.to_csv(pathname[24:], sep = '\t')


# Counter script
badcount = 0   
totcount = 0

for pathname in iglob('T:\courses\MSiA400\Jobs\ex*log'):

    # Read each data file
    with open(pathname, 'r') as f:
        file = f.readlines()
        fields = file[3].split()[1:]
        data = file[4:]
        
        # Total row count
        totcount += len(data)
        
        
        for i, row in enumerate(data):
            l = row.split()
            data[i] = l
        
        # Create data frame
        df = pd.DataFrame(data, columns = fields)
        
        bad = len(df[(df['time-taken'].str.isnumeric() == False)].index)
        badcount += bad
         
print(badcount) # 1,182,218
print(totcount) # 101,258,365
print(badcount / totcount * 100) # 1.17%


