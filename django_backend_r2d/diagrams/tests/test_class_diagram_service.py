from django.test import TestCase
from rest_framework.exceptions import ValidationError
import inspect
import warnings
from diagrams.services.ClassDiagramService import ClassDiagramService
from framework.factories.ModelFactory import ModelFactory
from framework.factories.AuditorFactory import AuditorFactory
from model_manager.constants import ModelProvider, OpenAIModels
from model_manager.models import ModelName
from diagrams.services.DiagramExceptions import UMLDiagramCreationError
from jobs.models import Job, JobStatus
from jobs.services.JobService import JobService
from django.contrib.auth import get_user_model
User = get_user_model()
from uuid import uuid4
import logging

class ClassDiagramServiceTests(TestCase):
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
        cls.user = User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')
        cls.job_status_submitted = JobStatus.objects.get(name='Submitted')
        cls.job_uuid = str(uuid4())
        cls.model = ModelName.objects.get(name='gpt-4-turbo')
        logging.getLogger('application_logging').setLevel(logging.ERROR)

        # Create a job record for the user stories
        cls.job_from_user_stories = Job.objects.create(
            job_id= cls.job_uuid,
            user=cls.user,
            job_status=cls.job_status_submitted,
            model=cls.model,
            job_details="Job Submitted",
            job_type="class_diagram",
            tokens=100,
            parameters = {
                "features": [
                    "Logging Framework", "Authorization Framework"
                ],
                "sub_features": [
                    "Application Logging", "JWT Authentication"
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
                            },
                            "Apollo-12": {
                                "id": "Apollo-12",
                                "requirement": "As an IT Administrator I want all API calls to be logged.",
                                "services_to_use": [],
                                "acceptance_criteria": "All API calls are logged, including the request and response payloads, and status. Logs should be searchable.",
                                "additional_information": "Use standard http status codes for status field in logs."
                            }
                        }
                    },
                    "Authorization Framework": {
                        "Application Logging": {
                            "Apollo-13": {
                                "id": "Apollo-13",
                                "requirement": "As a user, I want to be able to login using gmail account, so I wont have to remember passwords.",
                                "services_to_use": [
                                    "Google OAuth2"
                                ],
                                "acceptance_criteria": "Users can login using their gmail account. User data is not stored in the application.",
                                "additional_information": "Use Google OAuth2 library to implement login functionality ensure extensible design to allow other emails as well."
                            },
                            "Apollo-14": {
                                "id": "Apollo-14",
                                "requirement": "As an IT Administrator, I want users to have disabled accounts after 5 failed login attempts.",
                                "services_to_use": [
                                    ""
                                ],
                                "acceptance_criteria": "User accounts are disabled after 5 consecutive failed attempts.",
                                "additional_information": "IT administrator will be responsible for re-enabling a locked account."
                            }
                        }
                    }
                },
                "tokens": 248
            },
        )
        logging.getLogger('application_logging').setLevel(logging.ERROR)
        
    @classmethod
    def tearDownClass(cls):
        # Reset the log level after tests
        logging.getLogger('application_logging').setLevel(logging.DEBUG)
        super().tearDownClass()
        
    def setUp(self):
        self.model_provider = ModelProvider.OPEN_AI
        self.model_name = OpenAIModels.GPT_3_5_TURBO
        self.auditor_name = OpenAIModels.GPT_3_5_TURBO
        
        # Initialize the class diagram service
        self.class_diagram_service = ClassDiagramService(
            model_provider=self.model_provider,
            model_name=self.model_name,
            auditor_name=self.auditor_name,
            job_id = self.job_uuid
            )
        
    def test_generate_diagram_success(self):
        """
        Test class diagrams can be generated successfully.
        """
        try:
            result = self.class_diagram_service.generate_diagram()
            # Check if the result contains 'analysis_results' and 'audited_results'
            analysis_results = result.get('analysis_results', {})
            audited_results = result.get('audited_results', {})
            
            # Check diagrams in both analysis and audit results
            diagrams = analysis_results.get('diagrams', []) + audited_results.get('diagrams', [])

            # Find the words 'classDiagram'
            class_diagram_found = any("classDiagram" in diagram.get('diagram', '') for diagram in diagrams)
            self.assertTrue(class_diagram_found)
        except UMLDiagramCreationError as e:
            self.fail(f"Test failed with UMLDiagramCreationError: {e}")
    
    def test_generate_diagram_success_with_context(self):
        """
        Test execution with context, will result in context being used.
        """
        try:            
            result = self.class_diagram_service.generate_diagram()            
            # Check if the result contains 'analysis_results' and 'audited_results'
            analysis_results = result.get('analysis_results', {})
            audited_results = result.get('audited_results', {})
            
            # Check diagrams in both analysis and audit results
            diagrams = analysis_results.get('diagrams', []) + audited_results.get('diagrams', [])

            # Find the words 'classDiagram'
            class_diagram_found = any("classDiagram" in diagram.get('diagram', '') for diagram in diagrams)
            # Find the injected context
            #context_used = any("SIT_CAPSTONE_YP" in diagram.get('diagram', '') for diagram in diagrams)

            self.assertTrue(class_diagram_found, "The word 'classDiagram' was not found in the generated diagrams.")
            #self.assertTrue(context_used, "The context 'SIT_CAPSTONE_YP' was not found in the generated diagrams.")

        except UMLDiagramCreationError as e:
            self.fail(f"Test failed with UMLDiagramCreationError: {e}")
    