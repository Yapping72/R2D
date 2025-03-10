import inspect
from django.test import TestCase
from framework.daos.DjangoPostgresDaoFactory import DjangoPostgresDaoFactory
from accounts.daos.UserDAO import UserDao
import logging 

class DjangoPostgresDaoFactoryTestCase(TestCase):
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
        logging.getLogger('application_logging').setLevel(logging.ERROR)
        
    @classmethod
    def tearDownClass(cls):
        # Reset the log level after tests
        logging.getLogger('application_logging').setLevel(logging.DEBUG)
        super().tearDownClass()
        
    def test_create_user_dao(self):
        """
        Test that the factory returns an instance of UserDao when requested.
        """
        dao_instance = DjangoPostgresDaoFactory.get_dao('User')
        self.assertIsInstance(dao_instance, UserDao)

    def test_create_non_existent_dao(self):
        with self.assertRaises(ValueError):
            dao_instance = DjangoPostgresDaoFactory.get_dao('Model Doesnt Exist')
