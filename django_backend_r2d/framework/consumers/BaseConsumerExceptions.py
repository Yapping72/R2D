class BaseConsumerInitializationException(Exception):
    def __init__(self, message="Exception occurred while initializing BaseConsumer."):
        self.error_message = f"BaseConsumerInitializationException: {message}"
        super().__init__(self.error_message)
        
class BaseConsumerException(Exception):
    def __init__(self, message="Exception occurred in BaseConsumer."):
        self.error_message = f"BaseConsumerException: {message}"
        super().__init__(self.error_message)
