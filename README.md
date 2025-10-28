This script can use to bypass incoming port 25. Mail server incoming SMTP can set to other 25 port to receive email by the help of Lambda function

The Simple Flow
AWS SES ---> AWS S3 ---> AWS Lambda --> email server

AWS SES will receive the raw email then store to AWS S3 Bucket as JSON. there is a trigger on AWS S3 whenever there is add new item will run AWS Lambda. 
The Lambda function is get the new add JSON file then convert as raw email. After convertion then send the item to the Mail server using custom port

Requeirement
1. AWS SES
2. AWS S3
3. Email server with SMTP or MTA activate

Setting AWS SES as Incoming email server
1. Pointing MX record to AWS SES
2. Add rule for incoming email server

Deploy the python code to AWS Lambda
1. Add role to S3 and SES to the lambda function
2. Change the server parameter

Create Amazon S3
1. Create Amazon S3 Bucket
2. Add lambda function that created earlier
