import pandas as pd
import argparse
import os
from os.path import join
import re
from IPython.display import display
from IPython.display import Image
import sys
import csv

parser = argparse.ArgumentParser(description='Clean user logs for Vail Job Ads project')
parser.add_argument('--input_path', default='T:/courses/MSiA400/Jobs/', help='Path to directory containing data')
parser.add_argument('--output_path', default='Z:/vail/data/', help='Path to directory to store clean data')

def read_data(path):
    with open(path) as f:
        log_file = f.readlines()
        # Pulls column names that are on the fourth line of the file and tosses leading field indicator
        fields = log_file[3].split()[1:]
        # Pulls rows of starting that start on the fifth row of the file
        data = log_file[4:]
        # Splits data to be loaded into dataframe
        data = [row.split() for row in data]
        df = pd.DataFrame(data, columns=fields)
        # Removes rows that are incorrectly parsed (last field should be numeric, not string or null)
        df = df[(df['time-taken'].str.isnumeric() == True)]
        df['time'] = df['time'].replace('-', '')
        return df
    
def parse_ids(df):    
    # Splits out uri query into id fields
    df[['jvguid', 'buid', 'vsid', 'aguid']] = df['cs-uri-query'].str.split('&', expand=True).iloc[:, :4]
    # Remove type of id from field so all that's remaining is the actual id
    df['jvguid'] = df['jvguid'].str.replace(r'.*=', '')
    df['buid'] = df['buid'].str.replace(r'.*=', '')
    df['vsid'] = df['vsid'].str.replace(r'.*=', '')
    df['aguid'] = df['aguid'].str.replace(r'.*=', '')
    return df

def parse_referer(df):
    refer = []
    i = 0
    refer_group = [None]*len(df['cs(Referer)'])
    for url in df['cs(Referer)']:
        url = re.sub('https?://(www\.)?(m\.)?','',url)
        if bool(re.compile('(\.jobs?|jobs?\.)').search(url)):
            parts = re.split('(\.jobs?|jobs?\.)',url)
            if parts[0] == '':
                url = parts.pop()
            else:
                url = parts[0]
        if bool(re.compile('(\.com|\.org|\.net)').search(url)):
                   url = re.split('(\.com|\.org|\.net)',url)[0]
        if bool(re.compile('\.jobamatic').search(url)):
                   url = 'simplyhired'
        if bool(re.compile('(\.us|us\.)').search(url)):
                   url = 'government'
        if bool(re.compile('(\&|\.|\/)').search(url)):
                   #uk.append(url)
                   #index.append(i)
            refer_group[i] = 'unknown'
        if url == 'us':
            url = 'government'
        refer.append(url)
        i = i+1
    df['refer'] = refer
    return df

def new_jobs(path):
    # Create empty dataframe for new jobs and define columns
    new = pd.DataFrame()
    columns = ['JVGUID','DateNew','BUID','CompanyName','Title', 'OnetCode','Location','Link','a','b','c','d']
    # Walk through path folder and populate new jobs dataframe
    for root, dirs, files in os.walk(path):       
        for file in files: 
            if file.endswith("new.csv"):              
                 paths = os.path.join(root,file)
                 tables = pd.read_csv(paths, quotechar = '"',names = columns,encoding = "ISO-8859-1" )
                 new = new.append(tables.drop([0]),ignore_index=True)
    return new

def expired_jobs(path):
    # Create empty dataframe for expired jobs
    expired = pd.DataFrame()
    # Walk through path folder and populate expired jobs dataframe
    for root, dirs, files in os.walk(path):       
        for file in files: 
            if file.endswith("expired.csv"):              
                 paths = os.path.join(root,file)
                 tables = pd.read_csv(paths, quotechar = '"',names = ['JVGUID','ExpiredDate'],encoding = "ISO-8859-1" )
                 expired = expired.append(tables,ignore_index=True)
    return expired
        
def job_descriptions(path):
    # Create empty dataframe for job descriptions
    desc = pd.DataFrame()
    # Walk through path folder and populate expired jobs dataframe
    for root, dirs, files in os.walk(path):       
        for file in files: 
            if file.endswith("descriptions.csv"):              
                 paths = os.path.join(root,file)
                 tables = pd.read_csv(paths, quotechar = '"',names = ['JVGUID','Description'],encoding = "ISO-8859-1" )
                 desc = desc.append(tables,ignore_index = True)
    return desc    
    
def combine_jobs(new, expired, desc):
    # Combine all three data tables
    combined = pd.merge(desc, new, on='JVGUID', how='outer')
    jobs = pd.merge(combined, expired, on='JVGUID', how = 'left')
    # Create additional fields
    jobs['State'] = jobs['Location'].str[:2]
    jobs['City'] = jobs['Location'].str[3:]
    jobs['ExpiredDate'] = pd.to_datetime(jobs['ExpiredDate'])
    jobs['DateNew'] = pd.to_datetime(jobs['DateNew'])
    jobs['FullTimeDesc'] = jobs.Description.str.contains(r'full.?time',case=False)
    jobs['PartTimeDesc'] = jobs.Description.str.contains(r'part.?time',case=False)
    # Define top job titles
    jobtitles = ['Manager','Sale','Service','Engineer','Specialist','Assistant','Engineer','Specialist','Assistant','Associate','Tech','Senior','Nurse','Analyst','Representative','Customer','Retail','Account','Consultant','Business','Support','Project','Product','Develop','Manage','Operation','President','Software','Director','Admin','Financ','Clinical','Market','Office','Research']
    # Create flags for posts with the job titles defined above
    for jobtitle in jobtitles:
        jobs['Has' + jobtitle] = jobs.Title.str.contains(jobtitle, case = False)
    # Delete anormal splits in the data
    job_posting = jobs[jobs.a.isnull()]
    job_posting = job_posting.drop(['a', 'b','c','d'],axis=1)
    return job_posting

    
def main():
    args = parser.parse_args()
    input_path = args.input_path
    output_path = args.output_path
    
    # Run functions defined above to clean and load job postings datasets
    jobs = combine_jobs(new_jobs(input_path), expired_jobs(input_path), job_descriptions(input_path))
    jobs.to_csv('jobsposting.csv',index=False,quoting=csv.QUOTE_MINIMAL)
    # Run functions defined above to clean and load user click datasets
    for filename in os.listdir(input_path):
        if filename.endswith('.log'):
            try:
                user = read_data(join(input_path, filename))
                user = parse_ids(user)
                user = parse_referer(user)
                user.to_csv(join(output_path, filename), index=False)
                print(filename, "cleaned")
            except ValueError as e:
                print('Error:', e)
                print('File:', filename)
                continue
                 
if __name__ == "__main__":
    main()
