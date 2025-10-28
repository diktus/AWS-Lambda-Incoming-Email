🚀 Enhanced Email Reception: Bypassing Port 25 with AWS Lambda
This project provides a robust solution for receiving emails on a custom, non-standard port by leveraging AWS Simple Email Service (SES), S3, and Lambda. This is particularly useful in environments where the standard SMTP port 25 is blocked or restricted for incoming traffic.

⚙️ Architecture and Workflow
The system acts as a secure intermediary, transforming and forwarding emails to your private mail server on a custom port.

Simple Flow Diagram

AWS SES → AWS S3 → AWS Lambda → Your Mail Server (Custom Port)

Detailed Workflow

Incoming Email: AWS SES receives the incoming raw email.

Storage: SES is configured via an SES Receipt Rule to store the complete raw email data into a designated AWS S3 Bucket as a JSON object.

Trigger: An S3 Bucket Event Notification (a trigger) is activated every time a new email object is added to the bucket. This event invokes the AWS Lambda function.

Conversion & Forwarding: The Lambda function performs the following:

Retrieves the newly added JSON file from S3.

Extracts the original raw email content from the JSON.

Establishes a connection to your private Mail Server (SMTP/MTA) on a custom, non-25 port.

Sends the raw email content to your mail server for final delivery.

✅ Prerequisites
Before deployment, ensure you have the following components and settings:

AWS Account: With permissions to configure SES, S3, and Lambda.

AWS SES Setup: Activated for email receiving.

Your Mail Server: An operational mail server (MTA/SMTP service) that is configured to listen and accept emails on a custom port (e.g., port 2525, 587, etc.) accessible by the Lambda function.

🛠️ Setup and Deployment Steps
Follow these steps to deploy the solution:

1. Configure AWS SES for Incoming Mail

DNS Setup: Point your domain's MX record to the appropriate AWS SES endpoint (e.g., inbound-smtp.REGION.amazonaws.com).

Create Receipt Rule:

Define an AWS SES Receipt Rule Set for your domain.

Add a rule to store the email in a specific Amazon S3 Bucket.

2. Create Amazon S3 Bucket

Create a dedicated Amazon S3 Bucket to store the incoming raw emails. This is the bucket specified in the SES rule above.

3. Deploy and Configure AWS Lambda

Deploy Python Code: Deploy the provided Python script to a new AWS Lambda function.

Configure Lambda Permissions (IAM Role): The Lambda function's execution role must include:

s3:GetObject permission for the S3 bucket to retrieve the raw email file.

ses:SendRawEmail (optional, but good practice for error handling or alternative routing).

Set Environment/Server Parameters: Update the Lambda's configuration with your mail server details:

MAIL_SERVER_HOST: The hostname or IP address of your mail server.

MAIL_SERVER_PORT: The custom non-25 port your server is listening on.

4. Connect S3 and Lambda

In the S3 Bucket settings, add a Notification Event (S3 Trigger).

The event type should be ObjectCreated(All).

The destination should be the Lambda Function created in Step 3.
