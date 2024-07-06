import inspect
from django.test import TestCase

from django.contrib.auth import get_user_model
User = get_user_model()

from jobs.models import Job, JobStatus
from uuid import uuid4
from model_manager.models import ModelName
from diagrams.models import ClassDiagram    
from diagrams.serializers.ClassDiagramSerializer import ClassDiagramSerializer
from diagrams.services.ClassDiagramSavingService import ClassDiagramSavingService
from diagrams.services.DiagramExceptions import *

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
        cls.job = Job.objects.create(job_id=str(uuid4()), user=cls.user, job_status=cls.job_status, job_details="Test Job",tokens=100, parameters={})
        cls.model_name = ModelName.objects.get(name='gpt-3.5-turbo', code=3, provider='OpenAI')
        
    def setUp(self):
        self.data = {
            'job': self.job.job_id,
            'model_name_str': 'gpt-3.5-turbo',
            'feature': 'Authorization Framework',
            'diagram': 'classDiagram ...',
            'description': 'Example Description',
            'classes': 'Example Classes',
            'is_audited': False
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
        self.assertEqual(class_diagram.model_name.name, 'gpt-3.5-turbo')  # Correct field name
        self.assertEqual(class_diagram.feature, 'Authorization Framework')

    def test_class_diagram_serializer_invalid_model_name(self):
        """
        Test that the ClassDiagramSerializer raises a ValidationError for an invalid model_name.
        """
        self.data['model_name_str'] = 'invalid-model'
        serializer = ClassDiagramSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('model_name_str', serializer.errors)

    def test_class_diagram_saving_service(self):
        """
        Test the ClassDiagramSavingService to ensure it saves data correctly.
        """
        saving_service = ClassDiagramSavingService()
        try:
            saved_data = saving_service.save(self.data)
            self.assertIn('job', saved_data)
            self.assertIn('feature', saved_data)
            self.assertIn('diagram', saved_data)
            self.assertIn('description', saved_data)
        except ClassDiagramSavingError as e:
            self.fail(f"Saving service failed with error: {e}")