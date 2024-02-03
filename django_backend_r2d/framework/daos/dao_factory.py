from abc import ABC, abstractmethod
from django.db import models
from  accounts.daos.UserDAO import UserDao

class BaseDaoFactory(ABC):
    @abstractmethod
    def get_dao(self, model:models):
          raise NotImplementedError("Subclasses of BaseDaoFactory must implement get_dao().")

class DjangoPostgresDaoFactory(BaseDaoFactory):
    @staticmethod
    def get_dao(model):
        if model == 'User':
            return UserDao()
        else:
            raise ValueError(f"No DAO found for the model {model} provided.")