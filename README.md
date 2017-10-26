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

19.  JVGUID - which is currently in the form of GUID
20.  DateNew
21.  DateExpired
22.  BUID - company id
23.  CompanyName
24.  Title - Job title
25.  OnetCode
26.  Location - split into State, City
27.  Link - url of job site
28.  Description - will try to parse out additional information such as EducationRequired, Requirements, WorkExperience, Skills
  
