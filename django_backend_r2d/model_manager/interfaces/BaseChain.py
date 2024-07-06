from abc import ABC, abstractmethod

class BaseChain(ABC):
    """
    Defines the interface for a chain that can be used within R2D.
    """
    @abstractmethod
    def execute_chain(self):
        """
        Chains the responses from a model to an auditor.  
        raises:
            AnalyzeAndAuditChainException: If an error occurs during the chain.
        """
        pass
