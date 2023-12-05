import unittest

from src.database_manager import DatabaseManager
from src.user_manager import UserManager


class TestUserManager(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.db_manager = DatabaseManager('users.sqlite3')
        self.user_manager = UserManager(self.db_manager)

    def test_validate_credentials_success(self):
        result = self.user_manager.validate_credentials(
            {"login": "brenda74@example.org",
             "password": "+vJCXfFLe0"}, admin=True)
        self.assertTrue(result)

    def test_validate_credentials_failure(self):
        result = self.user_manager.validate_credentials(
            {"login": "brenda74@example.org", "password": "xyz"}, admin=True)
        self.assertFalse(result)
