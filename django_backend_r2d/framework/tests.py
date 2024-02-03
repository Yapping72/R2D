import inspect
from django.test import TestCase

from framework.daos.dao_factory import DjangoPostgresDaoFactory
from accounts.daos.UserDAO import UserDao


class DjangpoPostgresDaoFactoryTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Use inspect to get all methods of the class
        methods = inspect.getmembers(cls, predicate=inspect.isfunction)
        # Filter methods to only include those that start with 'test'
        test_methods = [method for method in methods if method[0].startswith('test')]
        # Count the test methods
        test_count = len(test_methods)
        print(f"\nExecuting {cls.__name__} containing {test_count} test cases")

    def test_create_user_dao(self):
        """
        Test that the factory returns an instance of UserDao when requested.
        """
        dao_instance = DjangoPostgresDaoFactory.get_dao('User')
        self.assertIsInstance(dao_instance, UserDao)

    def test_create_non_existent_dao(self):
        with self.assertRaises(ValueError):
            dao_instance = DjangoPostgresDaoFactory.get_dao('Model Doesnt Exist')
