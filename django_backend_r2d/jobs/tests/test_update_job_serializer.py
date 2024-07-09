# tests/test_serializers.py
from rest_framework import serializers
from django.test import TestCase
from jobs.models import Job
from jobs.serializers.UpdateJobStatusSerializer import UpdateJobStatusSerializer
import inspect
from jobs.models import Job, JobStatus
from django.contrib.auth import get_user_model
User = get_user_model()
from uuid import uuid4 
from model_manager.models import ModelName
import logging 

class UpdateJobSerializer(TestCase):
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
        
        cls.model = ModelName.objects.get(name='gpt-4-turbo')

        # Create a fake job
        cls.job_id = uuid4()
        cls.job = Job.objects.create(
            job_id= cls.job_id,
            user=cls.user,
            job_status=cls.job_status_submitted,
            job_details="Initial job details",
            tokens=100,
            parameters={},
            job_type="user_story",
            model=cls.model
        )
        logging.getLogger('application_logging').setLevel(logging.ERROR)
        
    @classmethod
    def tearDownClass(cls):
        # Reset the log level after tests
        logging.getLogger('application_logging').setLevel(logging.DEBUG)
        super().tearDownClass()
    
    def setUp(self):
        self.valid_data = {
            "job_id": self.job_id,
            "job_status": ""
        }
        
        self.invalid_job_id = {
            "job_id": uuid4(), # Use a random job id
            "job_status": "Draft"
        }
        
        self.invalid_job_status = {
            "job_id":  self.job_id,
            "job_status": "Invalid Status"
        }

    def test_update_job_serializer_with_valid_data(self):
        # Test the serializer with valid job status
        for valid_job_status in self.valid_job_status:
            self.valid_data['job_status'] = valid_job_status
            serializer = UpdateJobStatusSerializer(data=self.valid_data)
            self.assertTrue(serializer.is_valid())
            self.assertEqual(dict(serializer.validated_data), self.valid_data)

    def test_update_job_serializer_with_invalid_data(self):
        # Test serializer will throw correct exceptions if invalid data given
        serializer = UpdateJobStatusSerializer(data=self.invalid_job_id)
        self.assertFalse(serializer.is_valid())
        self.assertIn('job_id', serializer.errors)

        serializer = UpdateJobStatusSerializer(data=self.invalid_job_status)
        self.assertFalse(serializer.is_valid())
        self.assertIn('job_status', serializer.errors)

