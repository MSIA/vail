/* SQL queries below create and populate two tables for the jobs datasets */

-- Set role to ensure other people have access to the database
SET ROLE jobs2018;

-- Create a table for user clicks
CREATE TABLE user_click 
(
	click_date date,
	click_time time,
	computer_name varchar(255),
	method varchar(255),
	uri_stem varchar(255),
	uri_query text,
	ip varchar(255),
	version varchar(255),
	agent text,
	cookie varchar(255),
	referer text,
	host varchar(255),
	status varchar(255),
	substatus varchar(255),
	win32_status varchar(255),
	sc_bytes varchar(255),
	cs_bytes varchar(255),
	time_taken int,
	jvguid varchar(255),
	buid varchar(255),
	vsid varchar(255),
	aguid varchar(255),
	refer text
);

-- Create a table for job postings
CREATE TABLE jobposting
(
    jvguid character(255),
    description text,
    newdate date,
    buid character(255),
    company character(255),
    jobtitle character(255),
    onetcode character(255),
    loc character(255),
    urllink text,
    expiredate date,
    stateloc character(3),
    cityloc character(255),
    fulltime boolean,
    parttime boolean,
    manager boolean,
    sale boolean,
    service boolean,
    engineer boolean,
    specialist boolean,
    assistant boolean,
    associate boolean,
    tech boolean,
    senior boolean,
    nurse boolean,
    analyst boolean,
    representative boolean,
    customer boolean,
    retail boolean,
    account boolean,
    consultant boolean,
    business boolean,
    support boolean,
    project boolean,
    product boolean,
    develop boolean,
    manage boolean,
    operation boolean,
    president boolean,
    software boolean,
    director boolean,
    has_admin boolean,
    finance boolean,
    clinical boolean,
    market boolean,
    office boolean,
    research boolean
);

/* 
Change the directory in command line to the folder that contains the data and run the following code:

for x in $(ls *.log); do psql -h pg -c "\copy user_click from $x csv header" -d jobs2018; done

To code above will load all files into our database. Be sure to type out the code above instead of copying and pasting.
*/

-- Because of data issues uncovered during EDA, we created a view to limit our data to be between March and May 2014
ALTER TABLE user_click RENAME TO user_click_old;

CREATE VIEW user_subset AS SELECT * FROM user_click_old WHERE click_date BETWEEN '03/01/2017' AND '05/31/2017';


