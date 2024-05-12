from abc import ABC, abstractmethod

class EmailNotificationInterface(ABC):
    @abstractmethod
    def send_email(self,receiver,header,body):
        """Sends an email"""
        pass
