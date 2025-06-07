## DevOps Challenge: Day 3 (NBA Data Lake for analytics)

### Project Overview
This is a project that extract data from an API call, and store it in AWS S3 bucket.
Also create a database with glue, and attach it with S3, finally it is created a query with Athena.

**Tools:**
- NBA Game API
- Cloud services (AWS S3, AWS Athena, AWS Glue)
- Python

**Prerequisites:**
- AWS account
- NBA API key

**Basic concept of the aws services used:**
- [AWS S3](https://docs.aws.amazon.com/s3/ "AWS S3") is used to store, manage, analyze, and protect any amount of data. It is for many use cases like data lakes, deploy static web pages, cloud native applications, mobile applications, among others.
- [AWS Athena](https://docs.aws.amazon.com/athena/ "AWS Athena") is a service to make queries in an easy way.
Athena is serverless, that means is no necessary configure o setup infrastructure, so you do not worry about that.
Athena is ideal for running SQL queries on data stored in S3 in formats like JSON, Parquet, or CSV. It is often used for ad-hoc querying and gaining quick insights without setting up a database.
It is very useful to analyze data, and integrate it with ML tools to predict what your business need.
- [AWS Glue](https://docs.aws.amazon.com/glue/ "AWS Glue") is a serverless data integration service that helps you prepare and transform data for analytics. It includes tools for ETL (Extract, Transform, Load) jobs and a Data Catalog for metadata management.
Glue is designed to build data pipelines, automate data transformation processes, and manage metadata for datasets stored in S3 or other sources. It enables you to clean and structure raw data for analytics.

I want to share with you a table that chat gpt did, and I think it is useful.
They can work together, Glue prepares and organizes the data, while Athena queries the data directly.
![chat-gpt-table](/images/chat-gpt-table.png)

### Steps

1. Create an AWS account [(create free account)](https://aws.amazon.com/es/free/?nc1=h_ls&all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=*all "(create free account)")
2. in the aws console, click in the cloud shell button to open a cloud shell terminal
![aws-console](/images/aws-console.png)
3. type `nano setup_nba_data_lake.py` in the shell console and enter
![shell1](/images/shell1.png)
4. go to the repository, copy the src/setup_nba_data_lake.py file in the terminal and type ctrl + x , then type y
(Note: ensure that your bucket name is unique, and create your api key, beacuse you will need it, in the next step)
![shell2](/images/shell2.png)
5. type `nano .env` in the shell console and enter
![shell3](/images/shell3.png)
6. go to the repository, copy src/.env file in the terminal, put your information, type ctrl +x, then type y
(Note: go to the api web page, create an api key, and put it here)
![shell4](/images/shell4.png)
7. type `pip install python-dotenv` to install the packages to use .env files
![shell5](/images/shell5.png)
8. now run the code, type `python setup_nba_data_lake.py` and check everything is ok
![shell5](/images/shell6.png)
9. now in the search bar type s3 and go to s3 service, and check the bucket created
![s3](/images/s3.png)
10. enter and review the files
![s3-2](/images/s3-2.png)
11. download the raw file
![s3-raw-data](/images/s3-raw-data.png)
12. open the raw file in vscode, and you can see that it is a huge file data
![s3-raw-data-vsc](/images/s3-raw-data.png)
13. in the serach bar type athena and click in launch query editor button and paste this query `SELECT FirstName, LastName, Position, Team FROM nba_players WHERE Position = 'PG';` , click in run and you can see the results of the query
![query](/images/query.png)

#### With love and grateful to people who creates these projects:
[Day 3 explanation](https://www.youtube.com/watch?v=RAkMac2QgjM "Day 3")

[Original code](https://github.com/alahl1/NBADataLake "original code")

[DevOps Challenges info](https://www.linkedin.com/posts/alicia-ahl_devopsallstarchallenge-devopsallstarchallenge-activity-7282773132455624705-VkDB?utm_source=share&utm_medium=member_desktop "DevOps Challenges info")

