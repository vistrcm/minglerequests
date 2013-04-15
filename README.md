mingle_requests
==============================
lib to make api requests to mingle


Requirements
------------
Python3.

* [requests](python-requests.org)
* lxml

You can find all python requirements in requirements.txt

Config
------
By default config file contains user credentials. ~/.mingle_requests

```
[http://server]
username=super_admin
password=very_long_password
```

Usage
-----
For now tool gets list of tickets from TICKETS_FILE (default: tickets.csv) and add this tickets to migle.

TICKETS_FILE - CSV file in format:
```
field_reserved,jira_id,name,estimate,field_reserved,field_reserved,field_reserved
```

example:

```
1234132,JIRA-1,compare server performance,2,80,Open,Jon Dow
1234123,JIRA-100,write jira wrapper,1,80,In Progress,Stanislav Vitko
1111111,JIRA-55,fix calendar bug,1,80,Open,Stanislav Vitko
```
