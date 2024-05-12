# Data generator
## Description
Console application that generates random rows to database of predefined schema. After it's run it asks user to select table to generate data to. There are 18 options - one for each table and one that allows to generate data to all tables. After that program asks to provide number of rows to generate to specified earlier tables. Then program generates data to these tables and additionally writes sql select statements to 'inserts.sql' file in ./generated_sql folder (if it doesn't exist, it is automatically created)

## How to run
To run program you can simply invoke `python ./main.py` in terminal while having it opened in root folder of project. It's good to have connection.json file consisting of connection data with filled following fields:
```
{
    "user":"",
    "password":"",
    "host":"",
    "port":"",
    "service_name":""
}
```
When this file doesn't exist program will ask user to provide there information via standard input. However in this case user will have to manually write all of these data every time program starts. When connection.json exists it will be used to connect to database automatically.