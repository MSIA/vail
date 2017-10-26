import pandas as pd
import argparse
import os
from os.path import join


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
        # Removes rows that are incorrectly parsed (less than 18 fields) and splits data to be loaded into dataframe
        data = [row.split() for row in data if len(row.split()) == 18]
        df = pd.DataFrame(data, columns=fields)
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
    """
    TO DO: Yuqing's function with go here
    """
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