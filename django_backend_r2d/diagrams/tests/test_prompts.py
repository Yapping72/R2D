from django.test import TestCase
from model_manager.interfaces.BasePromptTemplate import BasePromptTemplate
from langchain.prompts import PromptTemplate
from diagrams.prompts.MermaidDiagramPrompts import ClassDiagramPromptTemplate, ERDiagramPromptTemplate, StateDiagramPromptTemplate, SequenceDiagramPromptTemplate
import inspect

class PromptTemplateTests(TestCase):
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

    def setUp(self):
        self.job_parameters = {
            "Authorization Framework": {
                "JWT": {
                    "Story-13": {
                        "id": "Apollo-13",
                        "requirement": "As a user, I want to be able to login using gmail account so that I don't have to remember my passwords.",
                        "services_to_use": ["Google OAuth"],
                        "acceptance_criteria": "User should be able to login using gmail.",
                        "additional_information": ""
                    }
                }
            }
        }
        self.context = {"context": "Some additional context"}

    def test_class_diagram_prompt_without_context(self):
        """
        Test ClassDiagramPromptTemplate without context.
        """
        prompt = ClassDiagramPromptTemplate.get_prompt(self.job_parameters)
        self.assertIsInstance(prompt, str)
        self.assertIn("You are a systems design expert.", prompt)
        self.assertIn("Your task is to create comprehensive and detailed class diagrams based on the given user stories.", prompt)
        self.assertIn("Here are the user stories grouped by features:", prompt)
        self.assertIn(str(self.job_parameters), prompt)
        self.assertNotIn("Here is some additional context", prompt)

    def test_class_diagram_prompt_with_context(self):
        """
        Test ClassDiagramPromptTemplate with context.
        """
        prompt = ClassDiagramPromptTemplate.get_prompt(self.job_parameters, self.context)
        self.assertIsInstance(prompt, str)
        self.assertIn("You are a systems design expert.", prompt)
        self.assertIn("Your task is to create class diagrams based on the given user stories.", prompt)
        self.assertIn("Here is some additional context that should be incorporated in your design:", prompt)
        self.assertIn(str(self.job_parameters), prompt)

