from abc import ABC, abstractmethod

class JobQueueInterface(ABC):
    @abstractmethod
    def enqueue(self, **kwargs):
        """Adds a job to the queue"""
        pass

    @abstractmethod
    def dequeue(self, **kwargs):
        """Removes a job from the queue"""
        pass
    
    @abstractmethod
    def update_status(self, **kwargs):
        """Updates the status of a job in the queue"""
        pass

    @abstractmethod
    def update_consumer(self, **kwargs):
        """Updates the consumer of a job in the queue"""
        pass
