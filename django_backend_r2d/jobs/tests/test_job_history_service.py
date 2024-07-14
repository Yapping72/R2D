from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
import uuid
import inspect

from django.contrib.auth import get_user_model
User = get_user_model()
from jobs.models import Job, JobStatus, JobHistory
from model_manager.models import ModelName
import logging 

class TestJobHistoryService(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')
        cls.job_status_processing = JobStatus.objects.get(name='Processing')
        cls.job_status_draft = JobStatus.objects.get(name='Draft')
        cls.model = ModelName.objects.get(name='gpt-3.5-turbo')
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
        # Create a job with Draft status
        self.job = Job.objects.create(
            job_id=uuid.uuid4(),
            user=self.user,
            job_status=self.job_status_draft,
            job_details="Initial job details",
            tokens=100,
            parameters={},
            job_type='user_story',
            model=self.model
        )

    def test_job_creation_creates_job_history(self):
        # Check if a JobHistory entry is created when a Job is created
        job_history = JobHistory.objects.last()
        self.assertIsNotNone(job_history)
        self.assertEqual(job_history.job, self.job)
        self.assertEqual(job_history.user, self.user)
        self.assertIsNone(job_history.previous_status)
        self.assertEqual(job_history.current_status, self.job_status_draft)
        self.assertEqual(job_history.job_type, self.job.job_type)

    def test_job_status_update_creates_job_history(self):
        # Check if a JobHistory entry is created when a Job status is updated
        self.job.job_status = self.job_status_processing
        self.job.save()
        
        job_history = JobHistory.objects.last()
        self.assertIsNotNone(job_history)
        self.assertEqual(job_history.job, self.job)
        self.assertEqual(job_history.user, self.user)
        self.assertEqual(job_history.previous_status, self.job_status_draft)
        self.assertEqual(job_history.current_status, self.job_status_processing)
        self.assertEqual(job_history.job_type, self.job.job_type)