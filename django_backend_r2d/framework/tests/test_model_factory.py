import inspect
from django.test import TestCase
from framework.factories.ModelFactory import ModelFactory
from model_manager.constants import ModelProvider, OpenAIModels
from model_manager.llms.GPTModel import GPTModel
from model_manager.services.ModelExceptions import ModelInitializationError
import logging 

class ModelFactoryTestCases(TestCase):
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
        logging.getLogger('application_logging').setLevel(logging.ERROR)
        
    @classmethod
    def tearDownClass(cls):
        # Reset the log level after tests
        logging.getLogger('application_logging').setLevel(logging.DEBUG)
        super().tearDownClass()
        
    def test_create_openai_models(self):
        """
        Test factory can create openai text models.
        """
        model = ModelFactory.get_model(ModelProvider.OPEN_AI, OpenAIModels.GPT_4_TURBO)
        self.assertIsInstance(model, GPTModel)
        model = ModelFactory.get_model(ModelProvider.OPEN_AI, OpenAIModels.GPT_3_5_TURBO)
        self.assertIsInstance(model, GPTModel)

    def test_create_openai_models_from_str(self):
        """
        Test factory can create openai text models from string.
        """
        model = ModelFactory.get_model("openai", "gpt-4-turbo")
        self.assertIsInstance(model, GPTModel)
        model = ModelFactory.get_model("openai", "gpt-3.5-turbo")
        self.assertIsInstance(model, GPTModel)
        model = ModelFactory.get_model("openai", "text-embedding-3-large")
        self.assertIsInstance(model, GPTModel)
        model = ModelFactory.get_model("openai", "text-embedding-3-small")
    
    def test_create_openai_embeddings(self):
        """
        Test factory can create openai embeddings models.
        """
        model = ModelFactory.get_model(ModelProvider.OPEN_AI, OpenAIModels.TEXT_EMBEDDING_3_LARGE)
        self.assertIsInstance(model, GPTModel)
        model = ModelFactory.get_model(ModelProvider.OPEN_AI, OpenAIModels.TEXT_EMBEDDING_3_SMALL)
        self.assertIsInstance(model, GPTModel)

    def test_create_non_existent_models(self):
        with self.assertRaises(ModelInitializationError):
            model = ModelFactory.get_model("NonExistentProvider", OpenAIModels.GPT_3_5_TURBO)
        with self.assertRaises(ModelInitializationError):
            model = ModelFactory.get_model(ModelProvider.OPEN_AI, "NonExistentModel")  

    def test_create_from_string(self):
        model = ModelFactory.get_model("openai", "gpt-4-turbo")
        self.assertIsInstance(model, GPTModel)