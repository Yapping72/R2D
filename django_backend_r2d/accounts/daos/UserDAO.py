from framework.daos.daos import BaseDao
from accounts.models import User

class UserDao(BaseDao):
    model = User

    def find_by_username(self, username):
        """
        Retrieve a user by their username.

        :param username: The username of the user to retrieve.
        :return: The user with the specified username or None if not found.
        """
        try:
            return self.model.objects.get(username=username)
        except self.model.DoesNotExist:
            return None
    
    def find_by_role(self, role):
        """
        Retrieve all users with a specific role.

        :param role: The role to filter users by.
        :return: A queryset containing all users with the specified role.
        """
        return self.model.objects.filter(role=role)

