from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
import uuid
import inspect

from django.contrib.auth import get_user_model
User = get_user_model()
from jobs.models import Job, JobStatus, JobQueue
from jobs.services.JobQueueService import JobQueueService
from model_manager.models import ModelName
import logging 

class JobAPIEndpointTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')
        cls.job_status_submitted = JobStatus.objects.get(name='Submitted')
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
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.save_job_url = reverse('save-job')
        self.update_status_url = reverse('update-job-status')
        self.get_job_url = reverse('get-job')
        self.get_all_jobs_url = reverse('get-all-jobs')

    def authenticated_post(self, url, data):
        """Helper function for making authenticated POST requests."""
        return self.client.post(url, data, format='json', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_create_job(self):
        payload = {
            "job_id": "c1ddb856-70b1-4c87-8111-2fd8fb8b4abd",
            "user_id": "1234567",
            "job_status": "Draft",
            "job_details": "Failed to submit job",
            "job_type": "class_diagram",
            "model_name": "gpt-3.5-turbo",
            "tokens": 248,
            "parameters": {
                "features": [
                    "Logging Framework"
                ],
                "sub_features": [
                    "Application Logging",
                ],
                "job_parameters": {
                    "Logging Framework": {
                        "Application Logging": {
                            "Apollo-11": {
                                "id": "Apollo-11",
                                "requirement": "As a user, I want all my actions to be logged, so that I can trace back my activities for auditing and debugging purposes.",
                                "services_to_use": [
                                    "CloudWatch"
                                ],
                                "acceptance_criteria": "All user actions should be logged with a timestamp, user ID, and action details. Logs should be searchable.",
                                "additional_information": "Consider GDPR and other legal implications when logging user data."
                            }
                        }
                    }
                },
                "tokens": 248
            },
            "created_timestamp": "2024-06-16T06:55:05.452Z",
            "last_updated_timestamp": "2024-06-16T06:55:11.822Z"
        }
        data = {'payload': payload}
        response = self.authenticated_post(self.save_job_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['data']['job_id']), payload['job_id'])
        self.assertEqual(response.data['message'], "Job parameters saved successfully.")
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['status_code'], 200)

        job = Job.objects.get(job_id=payload['job_id'])
        self.assertEqual(job.job_details, payload['job_details'])
        self.assertEqual(job.job_status.name, 'Draft')

    def test_update_job_status(self):
        job = Job.objects.create(
            job_id=uuid.UUID("c1ddb856-70b1-4c87-8111-2fd8fb8b4abd"),
            user=self.user,
            job_status=self.job_status_draft,
            job_details="Initial job details",
            tokens=100,
            parameters={},
            job_type='user_story',
            model= self.model
        )

        payload = {
            "job_id": str(job.job_id),
            "job_status": "Processing"
        }
        data = {'payload': payload}
        response = self.authenticated_post(self.update_status_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['data']['job_id']), payload['job_id'])
        self.assertEqual(response.data['message'], "Job updated successfully.")
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['status_code'], 200)

        job.refresh_from_db()
        self.assertEqual(job.job_status.name, 'Processing')

    def test_get_one_job(self):
        job = Job.objects.create(
            job_id=uuid.UUID("c1ddb856-70b1-4c87-8111-2fd8fb8b4afe"),
            user=self.user,
            job_status=self.job_status_draft,
            job_details="Details for single job retrieval",
            tokens=150,
            parameters={},
            job_type="user_story",
            model= self.model
        )
        payload = {
            "job_id": str(job.job_id)
        }
        data = {'payload': payload}
        response = self.authenticated_post(self.get_job_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['data']['job_id']), str(job.job_id))
        
    def test_get_all_jobs(self):
        # Create two job instances
        job1 = Job.objects.create(
            job_id=uuid.uuid4(),
            user=self.user,
            job_status=self.job_status_draft,
            job_details="First job details",
            tokens=100,
            parameters={},
            model= self.model
        )
        
        job2 = Job.objects.create(
            job_id=uuid.uuid4(),
            user=self.user,
            job_status=self.job_status_draft,
            job_details="Second job details",
            tokens=150,
            parameters={},
            model= self.model
        )

        # Make authenticated request to get all jobs
        response = self.authenticated_post(self.get_all_jobs_url, {})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']['jobs']), 2)

        job_ids = [str(job1.job_id), str(job2.job_id)]
        response_job_ids = [str(job['job_id']) for job in response.data['data']['jobs']]

        # Check if the created job IDs match the IDs in the response
        self.assertCountEqual(response_job_ids, job_ids)

    def test_create_job_with_submitted_status_updates_queue(self):
        payload = {
            "job_id": "c1ddb856-70b1-4c87-8111-2fd8fb8b4abd",
            "user_id": str(self.user.id),
            "job_status": "Submitted",
            "job_details": "Submit job to queue",
            "job_type":"user_story",
            "model_name":"gpt-4-turbo",
            "tokens": 248,
            "parameters": {
                "features": [
                    "Logging Framework"
                ],
                "sub_features": [
                    "Application Logging",
                ],
                "job_parameters": {
                    "Logging Framework": {
                        "Application Logging": {
                            "Apollo-11": {
                                "id": "Apollo-11",
                                "requirement": "As a user, I want all my actions to be logged, so that I can trace back my activities for auditing and debugging purposes.",
                                "services_to_use": [
                                    "CloudWatch"
                                ],
                                "acceptance_criteria": "All user actions should be logged with a timestamp, user ID, and action details. Logs should be searchable.",
                                "additional_information": "Consider GDPR and other legal implications when logging user data."
                            }
                        }
                    }
                },
                "tokens": 248
            },
            "created_timestamp": "2024-06-16T06:55:05.452Z",
            "last_updated_timestamp": "2024-06-16T06:55:11.822Z"
        }
        data = {'payload': payload}
        response = self.authenticated_post(self.save_job_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['data']['job_id']), payload['job_id'])
        self.assertEqual(response.data['message'], "Job parameters saved successfully.")
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['status_code'], 200)

        job = Job.objects.get(job_id=payload['job_id'])
        self.assertEqual(job.job_details, payload['job_details'])
        self.assertEqual(job.job_status.name, 'Submitted')

        # Verify that the job was added to the JobQueue
        job_queue_entry = JobQueue.objects.get(job=job)
        self.assertEqual(job_queue_entry.status, self.job_status_submitted)
        self.assertEqual(job_queue_entry.job, job)

    def test_create_job_with_non_submitted_status_does_not_updates_queue(self):
        payload = {
            "job_id":str(uuid.uuid4()),
            "user_id": str(self.user.id),
            "job_status": "Draft",
            "job_details": "Failed to submit job",
            "job_type":"user_story", 
            "model_name":"gpt-4-turbo",
            "tokens": 248,
            "parameters": {
                "features": [
                    "Logging Framework"
                ],
                "sub_features": [
                    "Application Logging",
                ],
                "job_parameters": {
                    "Logging Framework": {
                        "Application Logging": {
                            "Apollo-11": {
                                "id": "Apollo-11",
                                "requirement": "As a user, I want all my actions to be logged, so that I can trace back my activities for auditing and debugging purposes.",
                                "services_to_use": [
                                    "CloudWatch"
                                ],
                                "acceptance_criteria": "All user actions should be logged with a timestamp, user ID, and action details. Logs should be searchable.",
                                "additional_information": "Consider GDPR and other legal implications when logging user data."
                            }
                        }
                    }
                },
                "tokens": 248
            },
            "created_timestamp": "2024-06-16T06:55:05.452Z",
            "last_updated_timestamp": "2024-06-16T06:55:11.822Z"
        }
        data = {'payload': payload}
        response = self.authenticated_post(self.save_job_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['data']['job_id']), payload['job_id'])
        self.assertEqual(response.data['message'], "Job parameters saved successfully.")
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['status_code'], 200)

        job = Job.objects.get(job_id=payload['job_id'])
        self.assertEqual(job.job_details, payload['job_details'])
        self.assertEqual(job.job_status.name, 'Draft')

        # Verify that the job was not added to the JobQueue
        with self.assertRaises(JobQueue.DoesNotExist):
            JobQueue.objects.get(job=job)

    def test_update_job_status_to_submitted_updates_queue(self):
        job = Job.objects.create(
            job_id= str(uuid.uuid4()),
            user=self.user,
            job_status=self.job_status_draft,
            job_details="Initial job details",
            tokens=100,
            parameters={},
            job_type="user_story",
            model=self.model
        )

        # Verify that the job is not in the JobQueue initially
        with self.assertRaises(JobQueue.DoesNotExist):
            JobQueue.objects.get(job=job)
        
        # Update job status to 'Submitted'
        payload = {
            "job_id": str(job.job_id),
            "job_status": "Submitted"
        }
        data = {'payload': payload}
        response = self.authenticated_post(self.update_status_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['data']['job_id']), payload['job_id'])
        self.assertEqual(response.data['message'], "Job updated successfully.")
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['status_code'], 200)

        job.refresh_from_db()
        self.assertEqual(job.job_status.name, 'Submitted')

        # Verify that the job was added to the JobQueue
        job_queue_entry = JobQueue.objects.get(job=job)
        self.assertEqual(job_queue_entry.status, self.job_status_submitted)
        self.assertEqual(job_queue_entry.job, job)