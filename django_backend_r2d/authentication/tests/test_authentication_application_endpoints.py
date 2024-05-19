from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import OTP
from ..services.OTPService import OTPService
import inspect

from django.contrib.auth import get_user_model

class AuthenticationAPIEndpointTests(APITestCase):
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
        User = get_user_model()
        self.signup_url = '/api/auth/signup/'
        self.login_url = '/api/auth/login/'
        self.verify_password = "/api/auth/verify-password/"
        self.otp_verify_url = '/api/auth/otp/'
        # Create a test user to verify login functionality
        self.test_user = User.objects.create_user(username='auth-test-mock-user', password='1234', email="mock-gmail@gmail.com")
        # Generating JWT for the created user
        refresh = RefreshToken.for_user(self.test_user)
        self.access_token = str(refresh.access_token)

    def authenticated_post(self, url, data):
        """Helper function for making authenticated POST requests."""
        return self.client.post(url, data, format='json', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_signup_creates_user(self):
        data = {
            'email':'testuser01@hotmail.com',
            'username': 'testuser01',
            'password': 'testUser01Password'
        }
        response = self.client.post(self.signup_url, data, format='json')
        User = get_user_model()
        created_user = User.objects.filter(username='testuser01').first()
        
        # Assert that a user was created
        self.assertIsNotNone(created_user, "User should have been created")

        # Assert that the email matches the input data
        self.assertEqual(created_user.email, data['email'], "The user's email does not match the expected value")

        # Assert that the username matches the input data
        self.assertEqual(created_user.username, data['username'], "The user's username does not match the expected value")

    def test_signup_returns_token(self):
        data = {
            'email':'testuser02@hotmail.com',
            'username': 'testuser02',
            'password': 'testUser02Password',
        }
        response = self.client.post(self.signup_url, data, format='json')
        # Assertions to check the response data
        self.assertEqual(response.status_code, 200, "The response status code should be 200") # Header check
        self.assertIn('access_token', response.data['data'], "Access token should be present in the response data") # data check
        self.assertTrue(response.data['data']['access_token'], "Access token should not be empty") # data check
        self.assertEqual(response.data['message'], 'User account creation was successful', "Response message does not match") # message check
        self.assertTrue(response.data['success'], "Response success flag should be True") # success status check
        self.assertEqual(response.data['status_code'], 200, "The body response status code should be 200") # status code check
    
    def test_login_returns_otp_prompt(self):
        data = {
            'username': 'auth-test-mock-user',
            'password': '1234'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, 200, "The header response status code should be 200")
        self.assertIn('user_id', response.data['data'])
        self.assertEqual(response.data['message'], 'Please verify your OTP')
        self.assertTrue(response.data['success'], "Response success flag should be True")
        self.assertEqual(response.data['status_code'], 200, "The body response status code should be 200")
        
        
    def test_login_with_wrong_password(self):
        data = {
            'username': 'auth-test-mock-user',
            'password': 'wrong_password'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, 401, "The header response status code should be 401")
        self.assertIn('error', response.data['data'])
        self.assertIn('AuthenticationError: Invalid Credentials Provided', response.data['data']['error'])
        self.assertEqual(response.data['message'], 'Authentication Error')
        self.assertFalse(response.data['success'], "Response success flag should be false")
        self.assertEqual(response.data['status_code'], 401, "The body response status code should be 401")
        

    def test_verify_correct_password(self):
        data = {
            'user_id': self.test_user.id,
            'password': 1234
        }
        response = self.authenticated_post(self.verify_password, data)
        self.assertEqual(response.status_code, 200, "The header response status code should be 200")
        self.assertIn('result', response.data['data'])
        self.assertTrue(response.data['data']['result'])
        self.assertEqual(response.data['message'], 'Your password has been verified')
        self.assertTrue(response.data['success'], "Response success flag should be True")
        self.assertEqual(response.data['status_code'], 200, "The body response status code should be 200")
        
    
    def test_verify_wrong_password(self):
        data = {
            'user_id': self.test_user.id,
            'password': 1235
        }
        response = self.authenticated_post(self.verify_password, data)
        self.assertEqual(response.status_code, 403, "The header response status code should be 403")
        self.assertIn('error', response.data['data'])
        self.assertIn('AuthorizationError: You are not authorized to perform this action', response.data['data']['error'])
        self.assertEqual(response.data['message'], 'Authorization Error')
        self.assertFalse(response.data['success'], "Response success flag should be false")
        self.assertEqual(response.data['status_code'], 403, "The body response status code should be 403")
    
    def test_login_correct_credentials_correct_otp(self):
        data = {
            'username': 'auth-test-mock-user',
            'password': '1234'
        }
        response = self.client.post(self.login_url, data, format='json')
        user_id = response.data['data']['user_id']
        self.assertIn('user_id', response.data['data'])
        # Update the existing OTP entry with a known OTP
        known_otp = '12345678'
        
        otp_service = OTPService()  # Initialize the OTPService
        hashed_known_otp = otp_service._hash_otp(known_otp)  # Hash the known OTP

        # Fetch the existing OTP entry
        otp_entry = OTP.objects.get(user=self.test_user)
        otp_entry.otp = hashed_known_otp
        otp_entry.save()
        
        otp_data = {
            'user_id': user_id,
            'otp': known_otp
        }
        otp_response = self.client.post(self.otp_verify_url, otp_data, format='json')
        
        self.assertEqual(otp_response.status_code, 200, "The header response status code should be 200")
        self.assertIn('access_token', otp_response.data['data'], "Access token should be present in the response data") # data check
        self.assertTrue(otp_response.data['data']['access_token'], "Access token should not be empty") # data check
        self.assertEqual(otp_response.data['message'], 'OTP Successfully verified, redirecting you to webpage.', "Response message does not match") # message check
        self.assertTrue(otp_response.data['success'], "Response success flag should be True") # success status check
        self.assertEqual(otp_response.data['status_code'], 200, "The body response status code should be 200") # status code check
    
    def test_login_correct_credentials_correct_otp(self):
        data = {
            'username': 'auth-test-mock-user',
            'password': '1234'
        }
        response = self.client.post(self.login_url, data, format='json')
        user_id = response.data['data']['user_id']
        self.assertIn('user_id', response.data['data'])

        otp_data = {
            'user_id': user_id,
            'otp': "12345678"
        }
        otp_response = self.client.post(self.otp_verify_url, otp_data, format='json')
        
        self.assertEqual(otp_response.status_code, 401, "The header response status code should be 401")
        self.assertIn('error', otp_response.data['data'], "Error should be present in the response data") # data check
        self.assertIn("AuthenticationError: Invalid OTP.", otp_response.data['data']['error'])
        self.assertEqual(otp_response.data['message'], 'Authentication Error', "Response message does not match") # message check
        self.assertFalse(otp_response.data['success'], "Response success flag should be False") # success status check
        self.assertEqual(otp_response.data['status_code'], 401, "The body response status code should be 401") # status code check
    