import inspect
from django.test import TestCase

from django.contrib.auth import get_user_model
User = get_user_model()

from jobs.models import Job, JobStatus
from uuid import uuid4
from model_manager.models import ModelName
from diagrams.models import ClassDiagram    
from diagrams.serializers.ClassDiagramSerializer import ClassDiagramSerializer
from diagrams.services.ClassDiagramRepository import ClassDiagramRepository
from diagrams.services.DiagramExceptions import *
import logging 

class SaveClassDiagramsTests(TestCase):
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
        cls.model_name = ModelName.objects.get(name='gpt-3.5-turbo', code=3, provider='OpenAI')
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
            "feature": ["Logging Framework", "Application Logging"],
            "diagram": "classDiagram\nclass Logger {\n    +logAction(userID: String, actionDetails: String)\n    +logAPICall(requestPayload: String, responsePayload: String, status: int)\n}\n\nclass CloudWatch {\n    +sendLog(logData: String)\n}\n\nclass SIT_CAPSTONE_YP {\n    +monitorLogs(logData: String)\n}\n\nLogger --> CloudWatch : Association\nLogger --> SIT_CAPSTONE_YP : Association\n\nclass UserActionLog {\n    -timestamp: Date\n    -userID: String\n    -actionDetails: String\n    +getTimestamp(): Date\n    +getUserID(): String\n    +getActionDetails(): String\n}\n\nclass APICallLog {\n    -timestamp: Date\n    -requestPayload: String\n    -responsePayload: String\n    -status: int\n    +getTimestamp(): Date\n    +getRequestPayload(): String\n    +getResponsePayload(): String\n    +getStatus(): int\n}\n\nLogger --> UserActionLog : Composition\nLogger --> APICallLog : Composition",
            "description": "The Logger class is responsible for logging user actions and API calls. It associates with CloudWatch and SIT_CAPSTONE_YP for sending and monitoring logs respectively. UserActionLog and APICallLog are composed within Logger to store log details.",
            "classes": ["Logger", "CloudWatch", "SIT_CAPSTONE_YP", "UserActionLog", "APICallLog"],
            "is_audited": False,
            "model_name": "gpt-4-turbo"
        }

    def test_class_diagram_serializer_valid_data(self):
        """
        Test that the ClassDiagramSerializer validates and saves valid data correctly.
        """
        serializer = ClassDiagramSerializer(data=self.data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        class_diagram = serializer.save()
        self.assertIsInstance(class_diagram, ClassDiagram)
        self.assertEqual(str(class_diagram.job.job_id), self.job.job_id)  # Compare using IDs
        self.assertEqual(class_diagram.model.name, self.data.get('model_name'))  # Correct field name
        self.assertEqual(class_diagram.feature, self.data.get('feature'))
        
    def test_class_diagram_serializer_invalid_model_name(self):
        """
        Test that the ClassDiagramSerializer raises a ValidationError for an invalid model_name.
        """
        self.data['model_name'] = 'invalid-model'
        serializer = ClassDiagramSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('model_name', serializer.errors)
        self.assertEqual(serializer.errors['model_name'][0], 'Model name is invalid.')

    def test_class_diagram_repository(self):
        """
        Test the ClassDiagramRepository to ensure it saves data correctly.
        """
        repo = ClassDiagramRepository()
        try:
            saved_data = repo.save(self.data)
            # Convert UUID to string for comparison
            saved_job_id = str(saved_data.get('job'))
            self.assertIn(self.data.get("job"), saved_job_id)
            self.assertEqual(self.data.get("feature"), saved_data.get("feature"))
            self.assertEqual(self.data.get("diagram"), saved_data.get("diagram"))
            self.assertEqual(self.data.get("description"), saved_data.get("description"))
            self.assertEqual(self.data.get("classes"), saved_data.get("classes"))
            self.assertEqual(self.data.get("is_audited"), saved_data.get("is_audited"))
                
        except ClassDiagramSavingError as e:
            self.fail(f"Saving service failed with error: {e}")
    
    def test_class_diagram_repository_save_diagram(self):
        """
        Test the ClassDiagramRepository save_diagram method.
        """
        repo = ClassDiagramRepository()
        chain_response = {
            "analysis_results": {
            "diagrams": [
                {
                "feature": ["Logging Framework", "Application Logging"],
                "diagram": "classDiagram\nclass Logger {\n    +logAction(userID: String, actionDetails: String)\n    +logAPICall(requestPayload: String, responsePayload: String, status: int)\n}\n\nclass CloudWatch {\n    +sendLog(logData: String)\n}\n\nclass SIT_CAPSTONE_YP {\n    +monitorLogs(logData: String)\n}\n\nLogger --> CloudWatch : Association\nLogger --> SIT_CAPSTONE_YP : Association\n\nclass UserActionLog {\n    -timestamp: Date\n    -userID: String\n    -actionDetails: String\n    +getTimestamp(): Date\n    +getUserID(): String\n    +getActionDetails(): String\n}\n\nclass APICallLog {\n    -timestamp: Date\n    -requestPayload: String\n    -responsePayload: String\n    -status: int\n    +getTimestamp(): Date\n    +getRequestPayload(): String\n    +getResponsePayload(): String\n    +getStatus(): int\n}\n\nLogger --> UserActionLog : Composition\nLogger --> APICallLog : Composition",
                "description": "The Logger class is responsible for logging user actions and API calls. It associates with CloudWatch and SIT_CAPSTONE_YP for sending and monitoring logs respectively. UserActionLog and APICallLog are composed within Logger to store log details.",
                "classes": ["Logger", "CloudWatch", "SIT_CAPSTONE_YP", "UserActionLog", "APICallLog"]
                },
                {
                "feature": ["Authorization Framework", "Application Logging"],
                "diagram": "classDiagram\nclass User {\n    -email: String\n    -failedLoginAttempts: int\n    +loginWithGoogle(email: String)\n    +incrementFailedLoginAttempts()\n    +resetFailedLoginAttempts()\n    +disableAccount()\n}\n\nclass GoogleOAuth2 {\n    +authenticate(email: String)\n}\n\nclass ITAdministrator {\n    +reenableAccount(user: User)\n}\n\nUser --> GoogleOAuth2 : Association\nUser --> ITAdministrator : Association",
                "description": "The User class handles login functionalities and tracks failed login attempts. It associates with GoogleOAuth2 for authentication and ITAdministrator for re-enabling disabled accounts.",
                "classes": ["User", "GoogleOAuth2", "ITAdministrator"]
                }
            ],
            "is_audited": False,
            "model_name": "gpt-4-turbo"
            },
            "audited_results": {
            "diagrams": [
                {
                "feature": ["Logging Framework", "Application Logging"],
                "diagram": "classDiagram\nclass Logger {\n    -logAction(userID: String, actionDetails: String)\n    -logAPICall(requestPayload: String, responsePayload: String, status: int)\n}\n\nclass CloudWatch {\n    -sendLog(logData: String)\n}\n\nclass SIT_CAPSTONE_YP {\n    -monitorLogs(logData: String)\n}\n\nclass UserActionLog {\n    -timestamp: Date\n    -userID: String\n    -actionDetails: String\n    +getTimestamp(): Date\n    +getUserID(): String\n    +getActionDetails(): String\n}\n\nclass APICallLog {\n    -timestamp: Date\n    -requestPayload: String\n    -responsePayload: String\n    -status: int\n    +getTimestamp(): Date\n    +getRequestPayload(): String\n    +getResponsePayload(): String\n    +getStatus(): int\n}\n\nLogger --|> CloudWatch : Association\nLogger --|> SIT_CAPSTONE_YP : Association\n\nLogger o-- UserActionLog : Composition\nLogger o-- APICallLog : Composition",
                "description": "The Logger class is responsible for logging user actions and API calls. It associates with CloudWatch and SIT_CAPSTONE_YP for sending and monitoring logs respectively. UserActionLog and APICallLog are composed within Logger to store log details.",
                "classes": ["Logger", "CloudWatch", "SIT_CAPSTONE_YP", "UserActionLog", "APICallLog"]
                },
                {
                "feature": ["Authorization Framework", "Application Logging"],
                "diagram": "classDiagram\nclass User {\n    -email: String\n    -failedLoginAttempts: int\n    +loginWithGoogle(email: String)\n    +incrementFailedLoginAttempts()\n    +resetFailedLoginAttempts()\n    +disableAccount()\n}\n\nclass GoogleOAuth2 {\n    +authenticate(email: String)\n}\n\nclass ITAdministrator {\n    +reenableAccount(user: User)\n}\n\nUser --> GoogleOAuth2 : Association\nUser --> ITAdministrator : Association",
                "description": "The User class handles login functionalities and tracks failed login attempts. It associates with GoogleOAuth2 for authentication and ITAdministrator for re-enabling disabled accounts.",
                "classes": ["User", "GoogleOAuth2", "ITAdministrator"]
                }
            ],
            "is_audited": True,
            "model_name": "gpt-3.5-turbo"
            }
        }
        try:
            repo.save_diagram(self.job.job_id, chain_response)
            saved_diagrams = ClassDiagram.objects.all()
            self.assertEqual(saved_diagrams.count(), 4)
            
        except ClassDiagramSavingError as e:
            self.fail(f"Saving service failed with error: {e}")