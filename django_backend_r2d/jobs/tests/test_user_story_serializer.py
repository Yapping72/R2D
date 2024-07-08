# tests/test_serializers.py
from rest_framework import serializers
from django.test import TestCase
from jobs.serializers.UserStorySerializer import UserStorySerializer
import inspect
import logging 

class UserStorySerializerTest(TestCase):
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
        
    def setUp(self):
        self.valid_data = {
            "id": "Apollo-11",
            "requirement": "As a user, I want all my actions to be logged, so that I can trace back my activities for auditing and debugging purposes.",
            "services_to_use": ["CloudWatch"],
            "acceptance_criteria": "All user actions should be logged with a timestamp, user ID, and action details. Logs should be searchable.",
            "additional_information": "Consider GDPR and other legal implications when logging user data.",
        }
        
        self.invalid_data = {
            "id": "",
            "requirement": "",
            "services_to_use": [],
            "acceptance_criteria": "",
            "additional_information": "",
        }

    def test_user_story_serializer_with_valid_data(self):
        serializer = UserStorySerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(dict(serializer.validated_data), self.valid_data)

    def test_user_story_serializer_with_invalid_data(self):
        serializer = UserStorySerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())

    def test_user_story_serializer_missing_required_field(self):
        invalid_data = self.valid_data.copy()
        del invalid_data['id']
        serializer = UserStorySerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('id', serializer.errors)

    def test_user_story_serializer_blank_additional_information(self):
        data = self.valid_data.copy()
        data['additional_information'] = ''
        serializer = UserStorySerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(dict(serializer.validated_data), data)
