import inspect
from django.test import TestCase

from accounts.models import User
from accounts.daos.UserDAO import UserDao

class UserDaoTestCase(TestCase):
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
        # Create a test user for testing purposes
        self.test_user = User.objects.create(username="test_user", email="test@example.com")

    def test_get_one(self):
        dao = UserDao()
        # Test retrieving an existing user
        user = dao.get_one(self.test_user.id)
        self.assertEqual(user.username, "test_user")
        # Test retrieving a non-existent user
        non_existent_user = dao.get_one(999)  # Provide a non-existent ID
        self.assertIsNone(non_existent_user)

    def test_get_all(self):
        dao = UserDao()
        
        # Test retrieving all users
        all_users = dao.get_all()
        self.assertGreaterEqual(len(all_users), 1)  # At least one user should exist

    def test_create(self):
        dao = UserDao()
        
        # Test creating a new user
        new_user_data = {
            "username": "new_user",
            "email": "new@example.com",
        }
        new_user = dao.create(**new_user_data)
        self.assertEqual(new_user.username, "new_user")

    def test_find_by_role(self):
        dao = UserDao()
        # Test creating users with different roles
        admin_user_data = {
            "username": "admin_user",
            "email": "admin@example.com",
            "role": "ADMINISTRATOR",  # Specify the role here
        }
        normal_user_data = {
            "username": "normal_user",
            "email": "normal@example.com",
            "role": "NORMAL_USER",  # Specify the role here
        }

        admin_user = dao.create(**admin_user_data)
        normal_user = dao.create(**normal_user_data)

        # Check if the roles are set correctly
        self.assertEqual(admin_user.role, "ADMINISTRATOR")
        self.assertEqual(normal_user.role, "NORMAL_USER")

        # Test retrieving users by role
        retrieved_admin_users = dao.find_by_role(role="ADMINISTRATOR")
        retrieved_normal_users = dao.find_by_role(role="NORMAL_USER")

        # Check if the retrieved users match the created users
        self.assertIn(admin_user, retrieved_admin_users)
        self.assertIn(normal_user, retrieved_normal_users)

        # Test retrieving users by username
        retrieved_admin_users = dao.find_by_username(username="admin_user")
        retrieved_normal_users = dao.find_by_username(username="normal_user")

        # Check if the retrieved users match the created users
        self.assertEqual(admin_user, retrieved_admin_users)
        self.assertEqual(normal_user, retrieved_normal_users)

    def test_update(self):
        dao = UserDao()
        
        # Test updating an existing user
        updated_data = {
            "username": "updated_user",
        }
        updated_user = dao.update(self.test_user.id, **updated_data)
        self.assertEqual(updated_user.username, "updated_user")

        # Test updating a non-existent user
        non_existent_user = dao.update(999, **updated_data)  # Provide a non-existent ID
        self.assertIsNone(non_existent_user)

    def test_delete(self):
        dao = UserDao()
        
        # Test deleting an existing user
        result = dao.delete(self.test_user.id)
        self.assertTrue(result)

        # Test deleting a non-existent user
        non_existent_user = dao.delete(999)  # Provide a non-existent ID
        self.assertFalse(non_existent_user)
