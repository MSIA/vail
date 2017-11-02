SET ROLE jobs2018;

CREATE TABLE user_click (
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

/* 
Change the directory in command line to the folder that contains the data and run the following code:

for x in $(ls *.log); do psql -h pg -c "\copy user_click from $x csv header" -d jobs2018; done

Be sure to type out the code above instead of copying and pasting
*/