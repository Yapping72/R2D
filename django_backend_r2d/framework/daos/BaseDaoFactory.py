from abc import ABC, abstractmethod
from django.db import models

class BaseDaoFactory(ABC):
    @abstractmethod
    def get_dao(self, model:models):
          raise NotImplementedError("Subclasses of BaseDaoFactory must implement get_dao().")

