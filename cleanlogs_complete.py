import pandas as pd
import argparse
import os
from os.path import join
import re

parser = argparse.ArgumentParser(description='Clean user logs for Vail Job Ads project')
parser.add_argument('--input_path', default='/team/courses/MSiA400/Jobs/', help='Path to directory containing data')
parser.add_argument('--output_path', default='/home/lab.analytics.northwestern.edu/lgardiner/z/vail/data/processed/', help='Path to directory to store clean data')

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
    refer=[]
    i=0
    refer_group=[None]*len(df['cs(Referer)'])
    for url in df['cs(Referer)']:
        url=re.sub('https?://(www\.)?(m\.)?','',url)
        if bool(re.compile('(\.jobs?|jobs?\.)').search(url)):
            parts = re.split('(\.jobs?|jobs?\.)',url)
            if parts[0]=='':
                url = parts.pop()
            else:
                url = parts[0]
        if bool(re.compile('(\.com|\.org|\.net)').search(url)):
                   url = re.split('(\.com|\.org|\.net)',url)[0]
        if bool(re.compile('\.jobamatic').search(url)):
                   url='simplyhired'
        if bool(re.compile('(\.us|us\.)').search(url)):
                   url='government'
        if bool(re.compile('(\&|\.|\/)').search(url)):
                   #uk.append(url)
                   #index.append(i)
            refer_group[i]='unknown'
        if url=='us':
            url='government'
        refer.append(url)
        i=i+1
    df['refer']=refer
    return df
    

def main():
    args = parser.parse_args()
    input_path = args.input_path
    output_path = args.output_path
    
    for filename in os.listdir(input_path):
        if filename.endswith('.log'):
            df = read_data(join(input_path, filename))
            df = parse_ids(df)
            df = parse_referer(df)
            df.to_csv(join(output_path, filename), index=False)
            print(filename, "cleaned")
                      
if __name__ == "__main__":
    main()