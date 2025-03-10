from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import os
from notification.services.EmailNotificationInterface import EmailNotificationInterface
from notification.services.NotificationExceptions import *
import logging
logger = logging.getLogger("application_logging") # Instantiate logger class

class SendGridEmailService(EmailNotificationInterface):
    def __init__(self): 
        self.api_key = os.getenv("SENDGRID_API_KEY")

    def send_email(self,receiver,header,body):
        try:
            sender = 'requirements2design@gmail.com'
            message = Mail(from_email=sender,to_emails=receiver,subject=header,html_content=body)
            sg = SendGridAPIClient(self.api_key)
            result = sg.send(message)
            logger.debug(f"{result}--{result.status_code} -- {result.body} -- {result.headers}")
            logger.debug(f"Email Sent to: {receiver}, {header}, {body}")
        except Exception as e:
            if hasattr(e, 'body'):
                logger.error(f"Error details: {e.body}")
            logger.error(f"Error sending email to {receiver} -- {e}")
            raise SendEmailNotificationError(e)

