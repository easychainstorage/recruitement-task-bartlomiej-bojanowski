import logging
import sqlite3
import sys

import pandas as pd


class DatabaseManager:
    """A class for managing database connections and executing SQL queries."""

    def __init__(self, database_name):
        """Initializes the DatabaseManager with the specified database.

        :params database_name: The name of the SQLite database file.
        """
        self.database_name = database_name
        self.logger = logging.getLogger(__name__)

    def sql_query(self, sql_query):
        """Executes a SQL query on the connected SQLite database.

        :param sql_query: A string containing the SQL query to be executed.
        :return: A pandas DataFrame containing the results of the SQL query.
        """
        try:
            with sqlite3.connect(
                f"file:{self.database_name}?mode=ro", uri=True
            ) as conn:
                return pd.read_sql(sql_query, conn)
        except Exception:
            self.logger.error(
                "Fail load database.\n"
                "Remeber of run first python script.py create_database.py"
            )
            sys.exit(0)
