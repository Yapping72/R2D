import inspect
from django.test import TestCase
from django.contrib.auth import get_user_model
from uuid import uuid4
from jobs.models import Job, JobStatus
from model_manager.models import ModelName
from diagrams.models import ClassDiagram, ERDiagram, SequenceDiagram
from diagrams.services.DiagramRetrievalService import DiagramRetrievalService
from diagrams.services.DiagramExceptions import ClassDiagramRetrievalError
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

        cls.user = User.objects.create_user(username='testuser', password='password')
        cls.job_status = JobStatus.objects.get(name='Draft', code=1) 
        cls.model_name = ModelName.objects.get(name='gpt-3.5-turbo')
        cls.job = Job.objects.create(
            job_id=str(uuid4()),
            user=cls.user,
            job_status=cls.job_status,
            job_details="Test Job",
            tokens=100,
            parameters={},
            model=cls.model_name
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
            job=self.job,
            feature=["Logging Framework"],
            diagram="x-->a",
            description="Test Class Diagram",
            classes=["Logger"],
            helper_classes=["Helper"],
            is_audited=False,
            model_name=self.model_name
        )
        self.er_diagram = ERDiagram.objects.create(
            job=self.job,
            feature=["Database Framework"],
            diagram="x-->a",
            description="Test ER Diagram",
            entities=["Entity"],
            is_audited=False,
            model_name=self.model_name
        )
        self.sequence_diagram = SequenceDiagram.objects.create(
            job=self.job,
            feature=["Workflow Framework"],
            diagram="x-->a",
            description="Test Sequence Diagram",
            actors=["Actor"],
            is_audited=False,
            model_name=self.model_name
        )

    def test_retrieve_all_diagrams(self):
        """
        Test the retrieve_all_diagrams method to ensure it retrieves all diagram types for a job.
        """
        result = self.service.retrieve_all_diagrams(self.job.job_id)
        self.assertIn("class_diagrams", result)
        self.assertIn("er_diagrams", result)
        self.assertIn("sequence_diagrams", result)
        
        # Check that each diagram type is returned as expected
        self.assertEqual(len(result["class_diagrams"]), 1)
        self.assertEqual(len(result["er_diagrams"]), 1)
        self.assertEqual(len(result["sequence_diagrams"]), 1)
        
        # Verify data integrity
        class_diagram = result["class_diagrams"][0]
        self.assertEqual(class_diagram["description"], "Test Class Diagram")
        self.assertEqual(class_diagram["feature"], ["Logging Framework"])

    def test_retrieve_diagram_class(self):
        """
        Test retrieve_diagram method for retrieving only class diagrams.
        """
        result = self.service.retrieve_diagram(self.job.job_id, "class")
        self.assertIn("class_diagrams", result)
        self.assertEqual(len(result["class_diagrams"]), 1)
        self.assertEqual(result["class_diagrams"][0]["feature"], ["Logging Framework"])

    def test_retrieve_diagram_invalid_type(self):
        """
        Test retrieve_diagram method with an invalid diagram type.
        """
        with self.assertRaises(ValueError):
            self.service.retrieve_diagram(self.job.job_id, "invalid")
