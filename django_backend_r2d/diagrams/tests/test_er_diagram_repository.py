import inspect
from django.test import TestCase

from django.contrib.auth import get_user_model
User = get_user_model()

from jobs.models import Job, JobStatus
from uuid import uuid4
from model_manager.models import ModelName
from diagrams.models import ERDiagram    
from diagrams.serializers.ERDiagramSerializer import ERDiagramSerializer
from diagrams.repository.ERDiagramRepository import ERDiagramRepository
from diagrams.services.DiagramExceptions import *
import logging 

class SaveERDiagramsTests(TestCase):
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
        cls.user = User.objects.create_user(username='testuser', password='password')
        cls.job_status = JobStatus.objects.get(name='Draft', code=1) 
        cls.model_name = ModelName.objects.get(name='gpt-3.5-turbo')
        cls.job = Job.objects.create(job_id=str(uuid4()), user=cls.user, job_status=cls.job_status, job_details="Test Job",tokens=100, parameters={},model=cls.model_name)
        logging.getLogger('application_logging').setLevel(logging.ERROR)
        
    @classmethod
    def tearDownClass(cls):
        # Reset the log level after tests
        logging.getLogger('application_logging').setLevel(logging.DEBUG)
        super().tearDownClass()
                
    def setUp(self):
        self.data = {
            "job": self.job.job_id,
            "feature": ["Logging Framework"],
            "diagram": "erDiagram\nUserLogger {\n    int user_id PK\n    datetime timestamp\n    string action_details\n}\nLogQuery {\n    int query_id PK\n    string request\n}\nERD_SIT_CAPSTONE_YP {\n    // Entity for monitoring logs in AWS CloudWatch\n}",
            "description": "Entities and relationships for Logging Framework:\n\nUserLogger: Represents logging user actions with user ID, timestamp, and action details.\nLogQuery: Represents querying and retrieving logs related to a request.\nERD_SIT_CAPSTONE_YP: Entity recommended for monitoring logs in AWS CloudWatch.",
            "entities": ["UserLogger", "LogQuery", "ERD_SIT_CAPSTONE_YP"],
            "is_audited": False,
            "model_name": "gpt-4-turbo"
        }

    def test_ER_diagram_serializer_valid_data(self):
        """
        Test that the ERDiagramSerializer validates and saves valid data correctly.
        """
        serializer = ERDiagramSerializer(data=self.data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        er_diagram = serializer.save()
        self.assertIsInstance(er_diagram, ERDiagram)
        self.assertEqual(str(er_diagram.job.job_id), self.job.job_id)  # Compare using IDs
        self.assertEqual(er_diagram.model.name, self.data.get('model_name'))  # Correct field name
        self.assertEqual(er_diagram.feature, self.data.get('feature'))
        
    def test_er_diagram_serializer_invalid_model_name(self):
        """
        Test that the ERDiagramSerializer raises a ValidationError for an invalid model_name.
        """
        self.data['model_name'] = 'invalid-model'
        serializer = ERDiagramSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('model_name', serializer.errors)
        self.assertEqual(serializer.errors['model_name'][0], 'Model name is invalid.')

    def test_er_diagram_repository(self):
        """
        Test the ERDiagramRepository to ensure it saves data correctly.
        """
        repo = ERDiagramRepository()
        try:
            saved_data = repo.save(self.data)
            # Convert UUID to string for comparison
            saved_job_id = str(saved_data.get('job'))
            self.assertIn(self.data.get("job"), saved_job_id)
            self.assertEqual(self.data.get("feature"), saved_data.get("feature"))
            self.assertEqual(self.data.get("diagram"), saved_data.get("diagram"))
            self.assertEqual(self.data.get("description"), saved_data.get("description"))
            self.assertEqual(self.data.get("entities"), saved_data.get("entities"))
            self.assertEqual(self.data.get("is_audited"), saved_data.get("is_audited"))
                
        except ERDiagramSavingError as e:
            self.fail(f"Saving service failed with error: {e}")
    
    def test_er_diagram_repository_save_diagram(self):
        """
        Test the ERDiagramRepository save_diagram method.
        """
        repo = ERDiagramRepository()
        chain_response = {
            "analysis_results": {
                "diagrams": [
                {
                    "feature": ["Logging Framework"],
                    "diagram": "erDiagram\nUserLogger {\n    int user_id PK\n    datetime timestamp\n    string action_details\n}\nLogQuery {\n    int query_id PK\n    string request\n}\nERD_SIT_CAPSTONE_YP {\n    // Entity for monitoring logs in AWS CloudWatch\n}",
                    "description": "Entities and relationships for Logging Framework:\n\nUserLogger: Represents logging user actions with user ID, timestamp, and action details.\nLogQuery: Represents querying and retrieving logs related to a request.\nERD_SIT_CAPSTONE_YP: Entity recommended for monitoring logs in AWS CloudWatch.",
                    "entities": ["UserLogger", "LogQuery", "ERD_SIT_CAPSTONE_YP"]
                },
                {
                    "feature": ["Application Logging"],
                    "diagram": "erDiagram\n",
                    "description": "No classes provided for Application Logging.",
                    "entities": []
                },
                {
                    "feature": ["Authorization Framework"],
                    "diagram": "erDiagram\nGmailLogin {\n    int user_id PK\n}\nCompanyEmailLogin {\n    int admin_id PK\n}\nJWT {\n    string token_id PK\n}",
                    "description": "Entities and relationships for Authorization Framework:\n\nGmailLogin: Represents allowing users to login using Gmail account.\nCompanyEmailLogin: Represents allowing IT administrators to login using company email account.\nJWT: Represents the token ID for authorization.",
                    "entities": ["GmailLogin", "CompanyEmailLogin", "JWT"]
                }
                ],
                "is_audited": False,
                "model_name": "gpt-3.5-turbo"
            },
            "audited_results": {
                "diagrams": [
                {
                    "feature": ["Logging Framework"],
                    "diagram": "erDiagram\nUserLogger {\n    int user_id PK\n    datetime timestamp\n    string action_details\n}\nLogQuery {\n    int query_id PK\n    string request\n}\nERD_SIT_CAPSTONE_YP {\n    // Entity for monitoring logs in AWS CloudWatch\n}",
                    "description": "Entities and relationships for Logging Framework:\n\nUserLogger: Represents logging user actions with user ID, timestamp, and action details.\nLogQuery: Represents querying and retrieving logs related to a request.\nERD_SIT_CAPSTONE_YP: Entity recommended for monitoring logs in AWS CloudWatch.",
                    "entities": ["UserLogger", "LogQuery", "ERD_SIT_CAPSTONE_YP"]
                }
                ],
                "is_audited": True,
                "model_name": "gpt-3.5-turbo"
            }
            }
        try:
            repo.save_diagram(self.job.job_id, chain_response)
            saved_diagrams = ERDiagram.objects.all()
            self.assertEqual(saved_diagrams.count(), 4)
            
        except ERDiagramSavingError as e:
            self.fail(f"Saving service failed with error: {e}")