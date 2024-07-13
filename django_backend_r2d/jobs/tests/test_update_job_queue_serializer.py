# tests/test_serializers.py
from rest_framework import serializers
from django.test import TestCase
from jobs.models import Job
from jobs.serializers.UpdateJobQueueStatusSerializer import UpdateJobQueueStatusSerializer
import inspect
from jobs.models import Job, JobStatus
from django.contrib.auth import get_user_model
User = get_user_model()
from uuid import uuid4 
from model_manager.models import ModelName
import logging 

class UpdateJobQueueSerializer(TestCase):
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
        cls.valid_job_status = ['Submitted', 'Processing', 'Error Failed to Process', 'Job Aborted', 'Completed']        
        cls.user = User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')
        cls.job_status_submitted = JobStatus.objects.get(name='Submitted')
        
        cls.model = ModelName.objects.get(name='gpt-3.5-turbo')

        # Create a fake job (signals will create a JobQueue)
        cls.job_id = uuid4()
        cls.job = Job.objects.create(
            job_id= cls.job_id,
            user=cls.user,
            job_status=cls.job_status_submitted,
            job_details="Initial job details",
            tokens=100,
            parameters={},
            job_type="state_diagram",
            model=cls.model
        )
        
        logging.getLogger('application_logging').setLevel(logging.ERROR)
        
    @classmethod
    def tearDownClass(cls):
        # Reset the log level after tests
        logging.getLogger('application_logging').setLevel(logging.DEBUG)
        super().tearDownClass()
    
    def setUp(self):
        self.without_consumer = {
            "job_id": self.job_id,
            "job_status": ""
        }
        
        self.with_consumer = {
            "job_id": self.job_id, # Use a random job id
            "job_status": "",
            "consumer": "StateDiagramConsumer"
        }

    def test_update_job_queue_without_consumer(self):
        # Test the serializer with valid job status
        for valid_job_status in self.valid_job_status:
            self.without_consumer['job_status'] = valid_job_status
            serializer = UpdateJobQueueStatusSerializer(data=self.without_consumer)
            self.assertTrue(serializer.is_valid())
            validated_data = serializer.validated_data
            self.assertEqual(validated_data['job_status'].name, valid_job_status)
            self.assertIsNone(validated_data.get('consumer'))
            
    def test_update_job_queue_with_consumer(self):
        # Test the serializer with valid job status
        for valid_job_status in self.valid_job_status:
            self.with_consumer['job_status'] = valid_job_status
            serializer = UpdateJobQueueStatusSerializer(data=self.with_consumer)
            self.assertTrue(serializer.is_valid())
            validated_data = serializer.validated_data
            self.assertEqual(validated_data['job_status'].name, valid_job_status)
            self.assertEqual(validated_data['consumer'], "StateDiagramConsumer")

