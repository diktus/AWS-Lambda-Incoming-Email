import os
import json
import boto3
import smtplib
from email.parser import BytesParser
from email.policy import default

def lambda_handler(event, context):
    # Get bucket name from environment variable
    bucket_name = os.getenv("BUCKET_NAME", "default-bucket-name")  # Replace "default-bucket-name" with a fallback if needed
    
    # Initialize S3 client
    s3 = boto3.client('s3')
    
    # Extract object key details from the event
    object_key = event['Records'][0]['s3']['object']['key']
    
    try:
        # Retrieve the email file from S3
        email_data = s3.get_object(Bucket=bucket_name, Key=object_key)
        raw_email = email_data['Body'].read()
        
        # Parse the email content
        email = BytesParser(policy=default).parsebytes(raw_email)
        sender = email['From']
        recipient = email['To']
        
        # Extract attachments
        attachments = []
        for part in email.iter_attachments():
            filename = part.get_filename()
            if filename:
                content = part.get_payload(decode=True)  # Decode the attachment content
                attachments.append((filename, content))
        
        # Log attachment details
        if attachments:
            for filename, content in attachments:
                print(f"Attachment found: {filename}, Size: {len(content)} bytes")
                # Optionally save the attachment to another S3 bucket or process it
        
        # SMTP server details (update with your email server)
        smtp_server = "email server IP or Domain"
        smtp_port = 26
        
        # Connect to the SMTP server and forward the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.sendmail(sender, recipient, raw_email)
        
        # Log success
        print(f"Email successfully forwarded from {sender} to {recipient}")
        return {
            'statusCode': 200,
            'body': json.dumps(f"Email forwarded from {sender} to {recipient}")
        }
    except Exception as e:
        # Log error
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }
