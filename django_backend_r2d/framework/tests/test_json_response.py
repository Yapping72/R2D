import inspect
from django.test import TestCase
from framework.response.response import JSONResponse

class JSONResponseTestCases(TestCase):
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
    
    def test_transform_method(self):
        # Test data
        data = {"key1": "value1", "key2": "value2"}
        message = "Test message"
        status = "OK"
        status_code = 200

        # Create a JSONResponse object
        json_response = JSONResponse(data, message, status, status_code)

        # Call the transform method
        response = json_response.transform()

        # Assertions to check if the transform method works correctly
        self.assertEqual(response.status_code, status_code)
        self.assertEqual(response.data, {
            "data": data,
            "message": message,
            "status": status,
        })

        # Check if the headers are set correctly
        self.assertEqual(response["HTTP_CODE"], str(status_code))
