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
    template_data = event.get('template_data', '{}')
    config_set = event.get('config_set', None)
    tags = event.get('tags', None)
    
    # backwords compadibility with older versions
    if(template_data == 'default'):
        template_data = '{}'
        
    #logger.info("test")

    kwargs = dict(
        Source=email_from,
        Destination={
            'ToAddresses': email_to
        },
        ReplyToAddresses=[
            email_from
        ],
        Template=template,        
        TemplateData=template_data,
        ConfigurationSetName=config_set,
        Tags=tags
    )
    
    try: 
        client = boto3.client('ses')
        response = client.send_templated_email(**{k: v for k, v in kwargs.items() if v is not None})
        statusCode = response['ResponseMetadata']['HTTPStatusCode']

    except Exception as e:
        logger.error(type(e)) 
        logger.error(e.args)
        logger.error(e) 
                
    return {
        'statusCode': statusCode,
        'results': response
    }
