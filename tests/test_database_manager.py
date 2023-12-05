import os
import unittest
import sqlite3

import pandas as pd

from src.database_manager import DatabaseManager


class TestDatabaseManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_db = 'test_database.db'
        with sqlite3.connect(cls.test_db) as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE test_table (id INTEGER, name TEXT)")
            cursor.execute("""INSERT INTO test_table (id, name)
                              VALUES (1, 'Alicja')""")
            cursor.execute("""INSERT INTO test_table (id, name)
                              VALUES (2, 'Patryk')""")

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.test_db)

    def test_sql_query(self):
        db_manager = DatabaseManager(self.test_db)
        result = db_manager.sql_query('SELECT * FROM test_table')
        expected = pd.DataFrame({'id': [1, 2], 'name': ['Alicja', 'Patryk']})
        pd.testing.assert_frame_equal(result, expected)
