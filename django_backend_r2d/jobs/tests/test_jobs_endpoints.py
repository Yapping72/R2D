import uuid
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from jobs.models import Job, JobStatus
import inspect

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class JobAPIEndpointTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')
        cls.job_status_submitted = JobStatus.objects.get(name='Submitted')
        cls.job_status_processing = JobStatus.objects.get(name='Processing')
        cls.job_status_draft = JobStatus.objects.get(name='Draft')

        # Use inspect to get all methods of the class
        methods = inspect.getmembers(cls, predicate=inspect.isfunction)
        # Filter methods to only include those that start with 'test'
        test_methods = [method for method in methods if method[0].startswith('test')]
        # Count the test methods
        test_count = len(test_methods)
        print(f"\nExecuting {cls.__name__} containing {test_count} test cases")
    
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
            "job_status": "Submitted",
            "job_details": "Failed to submit job",
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

    def test_update_job_status(self):
        job = Job.objects.create(
            job_id=uuid.UUID("c1ddb856-70b1-4c87-8111-2fd8fb8b4abd"),
            user=self.user,
            job_status=self.job_status_draft,
            job_details="Initial job details",
            tokens=100,
            parameters={},
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
        )
        job2 = Job.objects.create(
            job_id=uuid.uuid4(),
            user=self.user,
            job_status=self.job_status_draft,
            job_details="Second job details",
            tokens=150,
            parameters={},
        )

        # Make authenticated request to get all jobs
        response = self.authenticated_post(self.get_all_jobs_url, {})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']['jobs']), 2)

        job_ids = [str(job1.job_id), str(job2.job_id)]
        response_job_ids = [str(job['job_id']) for job in response.data['data']['jobs']]

        # Check if the created job IDs match the IDs in the response
        self.assertCountEqual(response_job_ids, job_ids)