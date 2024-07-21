import json
import logging
import requests
from datetime import datetime
import pytz
import os 

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Slack Webhook URL Configured in AWS Lambda Environment Variables
SLACK_WEBHOOK_URL=os.getenv("SLACK_WEBHOOK_CLOUDWATCH_ALARM") 

def format_timestamp(timestamp):
    """
    Format the timestamp to Singapore Time (SGT)
    """
    try:
        # Parse the original timestamp
        dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f%z")
        
        # Convert to Singapore Time (SGT)
        sgt = pytz.timezone('Asia/Singapore')
        dt_sgt = dt.astimezone(sgt)
        
        return dt_sgt.strftime("%Y-%m-%d %H:%M:%S %Z")
    except ValueError:
        return timestamp
        
def format_slack_message(message_details):
    """
    Format the Slack message using Block Kit
    """
    # Define emoji for alarm state
    alarm_state = f"IN ALARM :large_red_square:" if message_details.get("NewStateValue") == "ALARM" else f"{message_details.get('NewStateValue')} :large_green_square:"

    # Format the timestamp
    formatted_timestamp = format_timestamp(message_details.get('StateChangeTime', 'N/A'))
    
    # Create a list of blocks with the specified keys and renaming them
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*:rotating_light: CloudWatch Alarm Triggered :rotating_light:*"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Alarm Name:*"
                },
                {
                    "type": "mrkdwn",
                    "text": f"{message_details.get('AlarmName', 'N/A')}"
                }
            ]
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Alarm ARN:*"
                },
                {
                    "type": "mrkdwn",
                    "text": f"{message_details.get('AlarmArn', 'N/A')}"
                }
            ]
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Alarm State:*"
                },
                {
                    "type": "mrkdwn",
                    "text": f"{alarm_state}"
                }
            ]
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Metric Name:*"
                },
                {
                    "type": "mrkdwn",
                    "text": f"{message_details.get('Trigger', {}).get('MetricName', 'N/A')}"
                }
            ]
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Metric Namespace:*"
                },
                {
                    "type": "mrkdwn",
                    "text": f"{message_details.get('Trigger', {}).get('Namespace', 'N/A')}"
                }
            ]
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Timestamp:*"
                },
                {
                    "type": "mrkdwn",
                    "text": f"{formatted_timestamp}"
                }
            ]
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Reason:*"
                },
                {
                    "type": "mrkdwn",
                    "text": f"{message_details.get('NewStateReason', 'N/A')}"
                }
            ]
        },
        {
            "type": "divider"
        }
    ]
    
    return blocks

def send_slack_notification(message_details):
    try:
        # Format the message using Block Kit
        slack_message = {
            "blocks": format_slack_message(message_details)
        }
        
        response = requests.post(SLACK_WEBHOOK_URL, json=slack_message, headers={'Content-Type': 'application/json'})
        if response.status_code != 200:
            logger.error(f"Request to Slack returned an error {response.status_code}, the response is: {response.text}")
    except Exception as e:
        logger.error(f"Failed to send notification to Slack: {str(e)}")

def lambda_handler(event, context):
    """
    Lambda handler function to process incoming CloudWatch Alarm SNS messages
    Sends a notification to Slack with the parsed message details
    """
    try:
        # Log the entire incoming event
        logger.info("Received event: %s", json.dumps(event, indent=2))
        
        # Check if 'Records' key is present and not empty
        if 'Records' in event and len(event['Records']) > 0:
            # Extract the SNS message
            sns_message = event['Records'][0]['Sns']['Message']
            logger.info("SNS Message: %s", sns_message)
            
            # Parse the SNS message if it's a JSON string
            try:
                message_details = json.loads(sns_message)
                logger.info("Parsed SNS Message: %s", json.dumps(message_details, indent=2))
                
                # Send notification to Slack
                send_slack_notification(message_details)
                
                # Return the parsed SNS message as part of the response
                return {
                    'statusCode': 200,
                    'body': json.dumps(message_details)
                }
            except json.JSONDecodeError:
                logger.warning("SNS message is not a valid JSON string")
                
                # Send notification to Slack with raw message
                send_slack_notification({"message": sns_message})
                
                return {
                    'statusCode': 200,
                    'body': sns_message
                }
        else:
            logger.warning("No SNS Records found in the event")
            return {
                'statusCode': 400,
                'body': json.dumps('No SNS Records found in the event')
            }
    except Exception as e:
        logger.error("Error processing the event: %s", str(e))
        send_slack_notification({"error": str(e)})
        return {
            'statusCode': 500,
            'body': json.dumps('Internal Server Error')
        }
