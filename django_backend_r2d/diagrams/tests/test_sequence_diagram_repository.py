import inspect
from django.test import TestCase

from django.contrib.auth import get_user_model
User = get_user_model()

from jobs.models import Job, JobStatus
from uuid import uuid4
from model_manager.models import ModelName
from diagrams.models import SequenceDiagram    
from diagrams.serializers.SequenceDiagramSerializer import SequenceDiagramSerializer
from diagrams.repository.SequenceDiagramRepository import SequenceDiagramRepository
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
            "diagram": "sequenceDiagram\n    actor User\n    participant Controller as Logging Controller\n    participant CloudWatch as CloudWatch Logging Service\n    User->>+Controller: Perform Action [message]\n    Controller->>+CloudWatch: Log Action {userID, timestamp, actionDetails} [message]\n    CloudWatch-->>-Controller: Confirm Log Entry [response]\n    Controller-->>-User: Action Logged [response]\n    alt GDPR Compliance Check\n        Controller->>Controller: Verify User Data Anonymization [check]\n    end",
            "description": "This sequence diagram represents the logging process for user actions as specified in Apollo-11. It includes interactions between the user, a logging controller, and the CloudWatch logging service. The primary flow logs each action with details such as user ID and timestamp. An alternative flow checks for GDPR compliance by verifying data anonymization.",
            "actors": ["User", "Logging Controller", "CloudWatch Logging Service"],
            "is_audited": False,
            "model_name": "gpt-4-turbo"
        }

    def test_sequence_diagram_serializer_valid_data(self):
        """
        Test that the SequenceDiagramSerializer validates and saves valid data correctly.
        """
        serializer = SequenceDiagramSerializer(data=self.data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        sequence_diagram = serializer.save()
        self.assertIsInstance(sequence_diagram, SequenceDiagram)
        self.assertEqual(str(sequence_diagram.job.job_id), self.job.job_id)  # Compare using IDs
        self.assertEqual(sequence_diagram.model.name, self.data.get('model_name'))  # Correct field name
        self.assertEqual(sequence_diagram.feature, self.data.get('feature'))
        
    def test_sequence_diagram_serializer_invalid_model_name(self):
        """
        Test that the SequenceDiagramSerializer raises a ValidationError for an invalid model_name.
        """
        self.data['model_name'] = 'invalid-model'
        serializer = SequenceDiagramSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('model_name', serializer.errors)
        self.assertEqual(serializer.errors['model_name'][0], 'Model name is invalid.')

    def test_er_diagram_repository(self):
        """
        Test the SequenceDiagramRepository to ensure it saves data correctly.
        """
        repo = SequenceDiagramRepository()
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
                
        except SequenceDiagramSavingError as e:
            self.fail(f"Saving service failed with error: {e}")
    
    def test_sequence_diagram_repository_save_diagram(self):
        """
        Test the SequenceDiagramRepository save_diagram method.
        """
        repo = SequenceDiagramRepository()
        chain_response = {
            "analysis_results": {
            "diagrams": [
                {
                "feature": ["Logging Framework", "Application Logging", "Apollo-11"],
                "diagram": "sequenceDiagram\n    actor User\n    participant Controller as Logging Controller\n    participant CloudWatch as CloudWatch Logging Service\n    User->>+Controller: Perform Action\n    Controller->>+CloudWatch: Log Action {userID, timestamp, actionDetails}\n    CloudWatch-->>-Controller: Confirm Log Entry\n    Controller-->>-User: Action Logged\n    alt GDPR Compliance Check\n        Controller->>Controller: Verify User Data Anonymization\n    end",
                "description": "This sequence diagram represents the logging process for user actions as specified in Apollo-11. It includes interactions between the user, a logging controller, and the CloudWatch logging service. The primary flow logs each action with details such as user ID and timestamp. An alternative flow checks for GDPR compliance by verifying data anonymization.",
                "actors": ["User", "Logging Controller", "CloudWatch Logging Service"]
                },
                {
                "feature": ["Logging Framework", "Application Logging", "Apollo-12"],
                "diagram": "sequenceDiagram\n    actor ITAdmin\n    participant APIGateway as API Gateway\n    participant Logger as Logger Service\n    ITAdmin->>+APIGateway: Make API Call {requestDetails}\n    APIGateway->>+Logger: Log Request {request, status}\n    Logger-->>-APIGateway: Log Confirmed\n    APIGateway-->>-ITAdmin: API Response {responseDetails}\n    loop Error Handling\n        APIGateway->>APIGateway: Check for HTTP Status Errors\n    end",
                "description": "This sequence diagram illustrates the logging of API calls as outlined in Apollo-12. The IT administrator initiates an API call, which is logged by a logger service, including request details and status. The primary flow ends with the API gateway returning the response. A loop handles potential HTTP status errors, ensuring robust error management.",
                "actors": ["ITAdmin", "API Gateway", "Logger Service"]
                },
                {
                "feature": ["Authorization Framework", "JWT Authentication", "Apollo-13"],
                "diagram": "sequenceDiagram\n    actor User\n    participant OAuthService as Google OAuth2 Service\n    participant AuthController as Authentication Controller\n    User->>+AuthController: Request Login via Gmail\n    AuthController->>+OAuthService: Initiate OAuth\n    OAuthService-->>-AuthController: OAuth Token\n    AuthController-->>-User: Login Success\n    alt Extensible Design\n        AuthController->>AuthController: Prepare for Other Email Providers\n    end",
                "description": "This sequence diagram details the login process using Gmail as described in Apollo-13. The user requests to login via Gmail, which is handled by the authentication controller initiating OAuth with Google's service. The successful authentication returns an OAuth token, leading to a login success message. An alternative flow prepares the system for future extensions to other email providers.",
                "actors": ["User", "Google OAuth2 Service", "Authentication Controller"]
                },
                {
                "feature": ["Authorization Framework", "JWT Authentication", "Apollo-14"],
                "diagram": "sequenceDiagram\n    actor User\n    participant AuthSystem as Authentication System\n    User->>+AuthSystem: Attempt Login\n    loop Check Login Attempts\n        AuthSystem->>AuthSystem: Increment Attempt Count\n        alt Exceeded Attempts\n            AuthSystem->>AuthSystem: Disable Account\n        end\n    end\n    AuthSystem-->>-User: Login Result\n    alt Account Management\n        actor Admin\n        Admin->>+AuthSystem: Re-enable Account\n        AuthSystem-->>-Admin: Account Re-enabled\n    end",
                "description": "This sequence diagram shows the process for handling login attempts and account disabling as per Apollo-14. The user attempts to login, which triggers a loop in the authentication system to count login attempts. If attempts exceed five, the account is disabled. The primary flow returns the login result. An alternative flow allows an administrator to re-enable a locked account.",
                "actors": ["User", "Authentication System", "Admin"]
                }
            ],
            "is_audited": False,
            "model_name": "gpt-4-turbo"
            },
            "audited_results": {
            "diagrams": [
                {
                "feature": ["Logging Framework", "Application Logging", "Apollo-11"],
                "diagram": "sequenceDiagram\n    actor User\n    participant Controller as Logging Controller\n    participant CloudWatch as CloudWatch Logging Service\n    User->>+Controller: Perform Action [message]\n    Controller->>+CloudWatch: Log Action {userID, timestamp, actionDetails} [message]\n    CloudWatch-->>-Controller: Confirm Log Entry [response]\n    Controller-->>-User: Action Logged [response]\n    alt GDPR Compliance Check\n        Controller->>Controller: Verify User Data Anonymization [check]\n    end",
                "description": "This sequence diagram represents the logging process for user actions as specified in Apollo-11. It includes interactions between the user, a logging controller, and the CloudWatch logging service. The primary flow logs each action with details such as user ID and timestamp. An alternative flow checks for GDPR compliance by verifying data anonymization.",
                "actors": ["User", "Logging Controller", "CloudWatch Logging Service"]
                },
                {
                "feature": ["Logging Framework", "Application Logging", "Apollo-12"],
                "diagram": "sequenceDiagram\n    actor ITAdmin\n    participant APIGateway as API Gateway\n    participant Logger as Logger Service\n    ITAdmin->>+APIGateway: Make API Call {requestDetails} [message]\n    APIGateway->>+Logger: Log Request {request, status} [message]\n    Logger-->>-APIGateway: Log Confirmed [response]\n    APIGateway-->>-ITAdmin: API Response {responseDetails} [response]\n    loop Error Handling\n        APIGateway->>APIGateway: Check for HTTP Status Errors [check]\n    end",
                "description": "This sequence diagram illustrates the logging of API calls as outlined in Apollo-12. The IT administrator initiates an API call, which is logged by a logger service, including request details and status. The primary flow ends with the API gateway returning the response. A loop handles potential HTTP status errors, ensuring robust error management.",
                "actors": ["ITAdmin", "API Gateway", "Logger Service"]
                },
                {
                "feature": ["Authorization Framework", "JWT Authentication", "Apollo-13"],
                "diagram": "sequenceDiagram\n    actor User\n    participant OAuthService as Google OAuth2 Service\n    participant AuthController as Authentication Controller\n    User->>+AuthController: Request Login via Gmail [message]\n    AuthController->>+OAuthService: Initiate OAuth [message]\n    OAuthService-->>-AuthController: OAuth Token [response]\n    AuthController-->>-User: Login Success [response]\n    alt Extensible Design\n        AuthController->>AuthController: Prepare for Other Email Providers [preparation]\n    end",
                "description": "This sequence diagram details the login process using Gmail as described in Apollo-13. The user requests to login via Gmail, which is handled by the authentication controller initiating OAuth with Google's service. The successful authentication returns an OAuth token, leading to a login success message. An alternative flow prepares the system for future extensions to other email providers.",
                "actors": ["User", "Google OAuth2 Service", "Authentication Controller"]
                },
                {
                "feature": ["Authorization Framework", "JWT Authentication", "Apollo-14"],
                "diagram": "sequenceDiagram\n    actor User\n    participant AuthSystem as Authentication System\n    User->>+AuthSystem: Attempt Login [message]\n    loop Check Login Attempts\n        AuthSystem->>AuthSystem: Increment Attempt Count [count]\n        alt Exceeded Attempts\n            AuthSystem->>AuthSystem: Disable Account [action]\n        end\n    end\n    AuthSystem-->>-User: Login Result [response]\n    alt Account Management\n        actor Admin\n        Admin->>+AuthSystem: Re-enable Account [request]\n        AuthSystem-->>-Admin: Account Re-enabled [response]\n    end",
                "description": "This sequence diagram shows the process for handling login attempts and account disabling as per Apollo-14. The user attempts to login, which triggers a loop in the authentication system to count login attempts. If attempts exceed five, the account is disabled. The primary flow returns the login result. An alternative flow allows an administrator to re-enable a locked account.",
                "actors": ["User", "Authentication System", "Admin"]
                }
            ],
            "is_audited": True,
            "model_name": "gpt-3.5-turbo"
            }
        }
           
        try:
            repo.save_diagram(self.job.job_id, chain_response)
            saved_diagrams = SequenceDiagram.objects.all()
            self.assertEqual(saved_diagrams.count(), 8)
            
        except SequenceDiagramSavingError as e:
            self.fail(f"Saving service failed with error: {e}")