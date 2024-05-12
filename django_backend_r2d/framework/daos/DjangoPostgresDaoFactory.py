from django.db import models
from framework.daos.BaseDaoFactory import BaseDaoFactory
from accounts.daos.UserDAO import UserDao

class DjangoPostgresDaoFactory(BaseDaoFactory):
    @staticmethod
    def get_dao(model):
        if model == 'User':
            return UserDao()
        else:
            raise ValueError(f"No DAO found for the model {model} provided.")