import inspect
from django.test import TestCase
from django.contrib.auth import get_user_model
from uuid import uuid4
from jobs.models import Job, JobStatus
from model_manager.models import ModelName
from diagrams.models import ClassDiagram, ERDiagram, SequenceDiagram
from diagrams.services.DiagramRetrievalService import DiagramRetrievalService
from diagrams.services.DiagramExceptions import ClassDiagramRetrievalError
from authentication.services.AuthenticationExceptions import AuthorizationError
import logging

User = get_user_model()

class DiagramRetrievalServiceTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Use inspect to get all methods of the class
        methods = inspect.getmembers(cls, predicate=inspect.isfunction)
        test_methods = [method for method in methods if method[0].startswith('test')]
        test_count = len(test_methods)
        print(f"\nExecuting {cls.__name__} containing {test_count} test cases")

        cls.user = User.objects.create_user(username='testuser555', password='password')
        cls.job_status = JobStatus.objects.get(name='Draft', code=1) 
        cls.model_name = ModelName.objects.get(name='gpt-3.5-turbo')
        cls.class_diagram_job = Job.objects.create(
            job_id=str(uuid4()),
            user=cls.user,
            job_status=cls.job_status,
            job_details="Test Job",
            tokens=100,
            parameters={},
            model=cls.model_name,
            job_type="class_diagram"
        )
        
        cls.er_diagram_job = Job.objects.create(
            job_id=str(uuid4()),
            user=cls.user,
            job_status=cls.job_status,
            job_details="Test Job",
            tokens=100,
            parameters={},
            model=cls.model_name,
            job_type="er_diagram"
        )
        
        cls.sequence_diagram_job = Job.objects.create(
            job_id=str(uuid4()),
            user=cls.user,
            job_status=cls.job_status,
            job_details="Test Job",
            tokens=100,
            parameters={},
            model=cls.model_name,
            job_type="sequence_diagram"
        )
        
        cls.service = DiagramRetrievalService()
        logging.getLogger('application_logging').setLevel(logging.ERROR)
        
    @classmethod
    def tearDownClass(cls):
        logging.getLogger('application_logging').setLevel(logging.DEBUG)
        super().tearDownClass()

    def setUp(self):
        # Create sample diagrams in the database for retrieval
        self.class_diagram = ClassDiagram.objects.create(
            job=self.class_diagram_job,
            feature=["Logging Framework"],
            diagram="x-->a",
            description="Test Class Diagram",
            classes=["Logger"],
            helper_classes=["Helper"],
            is_audited=True,
            model=self.model_name
        )
        self.er_diagram = ERDiagram.objects.create(
            job=self.er_diagram_job,
            feature=["Database Framework"],
            diagram="x-->a",
            description="Test ER Diagram",
            entities=["Entity"],
            is_audited=True,
            model=self.model_name
        )
        self.sequence_diagram = SequenceDiagram.objects.create(
            job=self.sequence_diagram_job,
            feature=["Workflow Framework"],
            diagram="x-->a",
            description="Test Sequence Diagram",
            actors=["Actor"],
            is_audited=True,
            model=self.model_name
        )

    def test_retrieve_all_diagrams(self):
        """
        Test the retrieve_all_diagrams method to ensure it retrieves all diagram types for a job.
        """
        result = self.service.retrieve_all_diagrams(self.user, self.class_diagram_job.job_id)
        self.assertIn("class_diagrams", result)
        self.assertIn("er_diagrams", result)
        self.assertIn("sequence_diagrams", result)

        
        # Verify data integrity
        class_diagram = result["class_diagrams"][0]
        self.assertEqual(class_diagram["description"], "Test Class Diagram")
        self.assertEqual(class_diagram["feature"], ["Logging Framework"])

    def test_retrieve_diagram_class(self):
        """Test retrieve_diagram method for class diagrams."""
        result = self.service.retrieve_diagram(self.user,self.class_diagram_job.job_id, "class_diagram")
        self.assertIn("class_diagrams", result)
        self.assertEqual(result["class_diagrams"][0]["feature"], ["Logging Framework"])

    def test_retrieve_diagram_er(self):
        """Test retrieve_diagram method for ER diagrams."""
        result = self.service.retrieve_diagram(self.user, self.er_diagram_job.job_id, "er_diagram")
        self.assertIn("er_diagrams", result)
        self.assertEqual(result["er_diagrams"][0]["feature"], ["Database Framework"])

    def test_retrieve_diagram_sequence(self):
        """Test retrieve_diagram method for sequence diagrams."""
        result = self.service.retrieve_diagram(self.user, self.sequence_diagram_job.job_id, "sequence_diagram")
        self.assertIn("sequence_diagrams", result)
        self.assertEqual(result["sequence_diagrams"][0]["feature"], ["Workflow Framework"])


    def test_retrieve_diagram_for_others(self):
        """Test retrieving a diagram for a job_id not associated with the user.
        Expects an AuthorizationError to be raised.
        """
        with self.assertRaises(AuthorizationError):
            # Attempt to retrieve a diagram for a job owned by another user
            self.service.retrieve_diagram(self.user, str(uuid4()), "class_diagram")