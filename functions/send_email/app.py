from __future__ import print_function
import os
import json
import boto3
import logging
from pprint import pprint


# Remove extranious logging messages
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    statusCode = 500 # error default
    template = event['email_template']
    email_to = event['email_to'].split(',')
    email_from = event['email_from']
    config = event['email_config']
    template_data = event['template_data']

    #logger.info("test")

    try: 
        client = boto3.client('ses')
        response = client.send_templated_email(
            Source=email_from,
            Destination={
                'ToAddresses': email_to
            },
            ReplyToAddresses=[
                email_from
            ],
            #ConfigurationSetName=config,
            Template=template,        
            TemplateData="{}"
        )
        statusCode = response['ResponseMetadata']['HTTPStatusCode']

    except Exception as e:
        logger.error(type(e)) 
        logger.error(e.args)
        logger.error(e) 
                
    return {
        'statusCode': statusCode,
        'results': response
    }
