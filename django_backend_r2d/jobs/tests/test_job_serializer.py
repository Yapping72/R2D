# tests/test_serializers.py
from rest_framework import serializers
from django.test import TestCase
from jobs.models import Job
from jobs.serializers.JobSerializer import JobSerializer
import inspect
from jobs.models import Job, JobStatus
from django.contrib.auth import get_user_model
User = get_user_model()
from uuid import uuid4 
from model_manager.models import ModelName
import logging 

class JobSerializerTest(TestCase):
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
        cls.valid_job_status = ['Draft', 'Queued', 'Submitted', 'Error Failed to Submit', 'Processing', 'Error Failed to Process', 'Job Aborted', 'Completed']
        
        cls.user = User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')
        cls.job_status_submitted = JobStatus.objects.get(name='Submitted')
        
        cls.model = ModelName.objects.get(name='gpt-3.5-turbo')

        # Create a fake job
        cls.job_id_1 = uuid4()
        cls.job_id_2 = uuid4()
        logging.getLogger('application_logging').setLevel(logging.ERROR)
        
    @classmethod
    def tearDownClass(cls):
        # Reset the log level after tests
        logging.getLogger('application_logging').setLevel(logging.DEBUG)
        super().tearDownClass()
    
    def setUp(self):
        self.job_payload_without_tokens = {
            "job_id": self.job_id_1,
            "user": self.user.id,
            "job_status": "Draft", # Draft so that no signal is triggered
            "job_details": "Initial job details",
            "parameters": {"key1": "abc, def, ghi", "key2": "abc, def, ghi"}, # 8 tokens
            "job_type": "class_diagram", # For testing purposes
            "model_name": "gpt-3.5-turbo"
        }
        
        self.job_payload_with_tokens = {
            "job_id": self.job_id_2,
            "user": self.user.id,
            "tokens": 10,
            "job_status": "Draft", # Draft so that no signal is triggered
            "job_details": "Initial job details",
            "parameters": {"key1": "abc, def, ghi", "key2": "abc, def, ghi"}, # 8 tokens
            "job_type": "class_diagram", # For testing purposes
            "model_name": "gpt-3.5-turbo"
        }

    def test_create_job_without_tokens(self):
        serializer = JobSerializer(data=self.job_payload_without_tokens)
        self.assertTrue(serializer.is_valid())
        job = serializer.save()
        self.assertEqual(job.tokens, 8)
    
    def test_create_job_with_tokens(self):
        serializer = JobSerializer(data=self.job_payload_with_tokens)
        self.assertTrue(serializer.is_valid())
        job = serializer.save()
        self.assertEqual(job.tokens, 10)
