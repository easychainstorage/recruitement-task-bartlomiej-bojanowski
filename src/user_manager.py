import logging
import sys


class UserManager:
    """
    A class for managing user authentication and executing
    SQL queries on a database.
    """

    def __init__(self, db_manager):
        """Initializes the UserManager with a database manager
        instance and a logger."""
        self.db_manager = db_manager
        self.logger = logging.getLogger(__name__)

    def validate_credentials(self, args, admin):
        """Validates user credentials in database.

        :param args: email or telephone number user and password
        :param admin: Boolean if account need to be admin
        :return: Boolean if the credentials are valid.
        """
        if admin:
            sql = f"""SELECT email, telephone_number, password, role FROM USERS
                      WHERE role='admin'
                      AND (email='{args['login']}'
                      OR telephone_number='{args['login']}')
                      AND password='{args['password']}'"""
        else:
            sql = f"""SELECT email, telephone_number, password FROM USERS
                      WHERE (email='{args['login']}'
                      OR telephone_number='{args['login']}')
                      AND password='{args['password']}'"""
        credentials = self.db_manager.sql_query(sql)
        return not credentials.empty

    def execute_query(self, sql_prompt):
        """
        Executes a given SQL query and returns the result.

        :param sql_prompt: A SQL query string
        :return: The result of the SQL query.
        """
        query_output = self.db_manager.sql_query(sql_prompt)
        if query_output.empty:
            self.logger.error("No result from database.")
            sys.exit(0)
        return self.db_manager.sql_query(sql_prompt)
