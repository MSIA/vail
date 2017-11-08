# vail
Vail group project for Everything Starts with Data MSiA 400

## Data Cleaning

The data consists of two types of files: user logs and job postings (see data dictionary below for information on fields). Before cleaning the data, you should create a directory to store your data within this project:

```
mkdir data
mkdir data/processed
```

To clean the user logs, run the following script and change the following argument to your output path:

```
python cleanlogs.py --output_path /home/lab.analytics.northwestern.edu/lgardiner/z/vail/data/processed
```

This will output a clean `.csv` file for every log text file in the original directory. 

## Jobs Postings Data

The jobsmerge.py file walks through the folder 'T:\courses\MSiA400\Jobs' which houses all of the raw Jobs postings data.  In the folder there are 3 types of files:
  New: job posting specifications
  Description: job posting descriptions
  Expired: which were made on a daily basis 
  
The code utilizes os.walk to go through each file in the folder and creates an aggregated data frame of each of the 3 types of files. Then it combines each of the three dataframes into a single aggregated jobs posting dataframe. 

*Note - The current merged file still contains tuples that were excessively split since there were commas housed within the columns.  This makes up <.001% of files (31,715 out of 4,810,306 entries) and will be fixed in future a iteration of this merge code. 

## Data Dictionary

### User Fields:

1.  date - the date the user viewed the job posting
2.  time - the time the user viewed the job posting
3.  s-computername
4.  cs-method
5.  cs-uri-stem
6.  cs-uri-query - provides JVGUID (job posting ID), BUID (company ID), VSID, AGUID (user ID)
7.  c-ip - user IP address
8.  cs-version
9.  cs(User-Agent)
10. cs(Cookie)
11. cs(Referer) - referral website (if any)
12. cs-host
13. sc-status
14. sc-substatus
15. sc-win32-status
16. sc-bytes
17. cs-bytes
18. time-taken - the time user spent on posting


### Job Posting Fields

19.  jvguid - which is currently in the form of GUID
20.  description - is the full text description of the job. Source for the boolean "fulltime" and "parttime"
21.  newdate - post date
21.  buid - company id
22.  company - company name
23.  jobtitle - job title
24.  onetcode
25.  loc - state-city
26.  urllink - url of job site
27.  expiredate - date of posting expiration
28.  stateloc - just state
29.  cityloc - just city
30.  fulltime - whether r'full.?time' is in the description field
31.  parttime - whether r'part.?time' is in the description field
32-46 Whether the word is found in the job title (ex. 'manager' attribute is true if the substring 'manager' is within the 'jobtitle' attribute 
 
  
