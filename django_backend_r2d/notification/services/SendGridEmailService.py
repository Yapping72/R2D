#from sendgrid import SendGridAPIClient
#from sendgrid.helpers.mail import Mail

import os
from notification.services.EmailNotificationInterface import EmailNotificationInterface
from notification.services.NotificationExceptions import *

class SendGridEmailService(EmailNotificationInterface):
    def __init__(self):
        pass
        # self.api_key = os.getenv("API_KEY")

    def send_email(self,receiver,header,body):
        try:
            sender = "R2D_OTP@gmail.com"
            # message = Mail(from_email=sender,to_emails=receiver,subject=header,html_content=body)
            # sg = SendGridAPIClient(self.api_key)
            # sg.send(message)
            print(f"Email Sent to: {receiver}, {header}, {body}")
        except Exception as e:
            raise SendEmailNotificationError()
