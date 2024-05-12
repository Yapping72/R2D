class SendEmailNotificationError(Exception):
    def __init__(self, message="Unspecified error occurred while trying to send email."):
        self.error_message = f"SendEmailNotificationError: {message}"
        super().__init__(self.error_message)
