import unittest
import re

from src.database_manager import DatabaseManager
from src.user_manager import UserManager
from src.account_actions import AccountActions


class TestUserManager(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.db_manager = DatabaseManager('users.sqlite3')
        self.user_manager = UserManager(self.db_manager)
        self.account_actions = AccountActions(self.user_manager)

    def test_invalid_login(self):
        result = self.account_actions.print_all_accounts(
            {"login": "736121560",
             "password": "n(9vNQ$jqO"}, admin=True)
        self.assertEqual(result, "Invalid Login")

    def test_print_all_accounts(self):
        result = self.account_actions.print_all_accounts(
            {"login": "brenda74@example.org",
             "password": "+vJCXfFLe0"}, admin=True)
        self.assertEqual(result, 84)

    def test_print_oldest_account(self):
        result = self.account_actions.print_oldest_account(
            {"login": "brenda74@example.org",
             "password": "+vJCXfFLe0"}, admin=True)
        self.assertEqual(result,
                         "name: Justin\n"
                         "email_adress: opoole@example.org\n"
                         "created_at: 2022-11-25 02:19:37")

    def test_group_by_age(self):
        result = self.account_actions.group_by_age(
            {"login": "brenda74@example.org",
             "password": "+vJCXfFLe0"}, admin=True)
        check_result = re.search("(?<=age: 9, count: )(.*)(?=\n)", result)
        self.assertEqual(check_result.group(), '5')

    def test_print_children(self):
        result = self.account_actions.print_children(
            {"login": "504140673",
             "password": "@9TcRo15As"}, admin=False)
        self.assertEqual(result, 'Jackie, 9\nMitchell, 6')

    def test_find_similar_children_by_age(self):
        result = self.account_actions.find_similar_children_by_age(
            {"login": "kcabrera@example.net",
             "password": "gk2VM$qk@S"}, admin=False)
        self.assertIn('Patricia, 636162531: Andrew, 4; James, 13', result)
        self.assertIn('Brandy, 686983157: Teresa, 4', result)
