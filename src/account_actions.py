class AccountActions:
    """
    A class for managing account actions for the users.
    """
    def __init__(self, user_manager):
        """
        Initializes the AccountActions with a UserManager instance.

        :param user_manager: UserManager class for handling user
        authentication and queries.
        """
        self.user_manager = user_manager

    def print_all_accounts(self, args, admin=True):
        """
        Prints the total number of user accounts.

        :param args: Arguments for user validation.
        :param admin: Flag to indicate if the operation requires
        admin privileges (default is True).
        :return: Total number of user accounts or
        an error message if validation fails.
        """
        sql_prompt = "SELECT COUNT(*) FROM USERS"
        if not self.user_manager.validate_credentials(args, admin):
            return "Invalid Login"
        result = self.user_manager.execute_query(sql_prompt)
        return result.iloc[0]['COUNT(*)']

    def print_oldest_account(self, args, admin=True):
        """
        Prints details of the oldest user account.

        :param args: Arguments for user validation.
        :param admin: Flag to indicate if the operation requires
        admin privileges (default is True).
        :return: A string containing the name, email address,
        and creation date of the oldest account,
        or an error message if validation fails.
        """
        sql_prompt = """SELECT firstname, email, created_at FROM USERS
                        ORDER BY created_at"""
        if not self.user_manager.validate_credentials(args, admin):
            return "Invalid Login"
        result = self.user_manager.execute_query(sql_prompt).iloc[0]
        console_output = "\n".join([f"name: {result['firstname']}",
                                    f"email_adress: {result['email']}",
                                    f"created_at: {result['created_at']}"])
        return console_output

    def group_by_age(self, args, admin=True):
        """
        Groups and counts children by age in the CHILDREN table.

        :param args: Arguments for user validation.
        :param admin: Flag to indicate if the operation requires
        admin privileges (default is True).
        :return: A string representing the count of children grouped by age,
        or an error message if validation fails.
        """
        if not self.user_manager.validate_credentials(args, admin):
            return "Invalid Login"
        sql_prompt = """SELECT age, COUNT(*) FROM CHILDREN
                        GROUP BY age
                        ORDER BY COUNT(*)"""
        result = self.user_manager.execute_query(sql_prompt)
        console_output = "\n".join([
            f"age: {rows['age']}, count: {rows['COUNT(*)']}"
            for iter, rows in result.iterrows()])
        return console_output

    def print_children(self, args, admin=False):
        """
        Prints the names and ages of user children.

        :param args: Arguments for user validation.
        :param admin: Flag to indicate if the operation requires
        admin privileges (default is True).
        :return: A string listing the names and ages of children,
        or an error message if validation fails.
        """
        if not self.user_manager.validate_credentials(args, admin):
            return "Invalid Login"
        sql_prompt = f"""SELECT CHILDREN.name, CHILDREN.age FROM CHILDREN
                         LEFT JOIN USERS ON
                         USERS.id_user = CHILDREN.index_parent
                         WHERE USERS.email='{args['login']}'
                         OR USERS.telephone_number ='{args['login']}'
                         ORDER BY CHILDREN.name"""
        result = self.user_manager.execute_query(sql_prompt)
        console_output = "\n".join(
            [f"{rows['name']}, {rows['age']}"
             for iter, rows in result.iterrows()]
        )
        return console_output

    def find_similar_children_by_age(self, args, admin=False):
        """
        Finds and prints children with similar ages
        to those associated with a user.

        :param args: Arguments for user validation.
        :param admin: Flag to indicate if the operation requires
        admin privileges (default is True).
        :return: A string listing similar children's names and ages,
        or an error message if validation fails.
        """
        if not self.user_manager.validate_credentials(args, admin):
            return "Invalid Login"
        age_children_prompt = f"""SELECT CHILDREN.age FROM CHILDREN
                                  LEFT JOIN USERS ON
                                  USERS.id_user = CHILDREN.index_parent
                                  WHERE USERS.email='{args['login']}'
                                  OR USERS.telephone_number
                                  ='{args['login']}'"""
        age_children_result = self.user_manager.execute_query(
            age_children_prompt)
        console_output = []
        if len(age_children_result) > 1:
            for iter, rows in age_children_result.iterrows():
                id_users_prompt = f"""SELECT USERS.id_user,
                                      USERS.telephone_number, USERS.firstname
                                      FROM CHILDREN LEFT JOIN USERS ON
                                      USERS.id_user = CHILDREN.index_parent
                                      WHERE CHILDREN.age = {rows['age']}
                                      ORDER BY CHILDREN.name"""
                id_users_prompt_result = self.user_manager.execute_query(
                    id_users_prompt)
                for iter, rows in id_users_prompt_result.iterrows():
                    children_prompt = f"""SELECT CHILDREN.name, CHILDREN.age
                                          FROM CHILDREN LEFT JOIN USERS ON
                                          USERS.id_user = CHILDREN.index_parent
                                          WHERE {rows['id_user']} =
                                          CHILDREN.index_parent
                                          ORDER BY CHILDREN.name"""
                    children_prompt_result = self.user_manager.execute_query(
                        children_prompt)
                    output = "; ".join(
                        [
                            f"{row['name']}, {row['age']}"
                            for _, row in children_prompt_result.iterrows()
                        ]
                    )
                    console_output.append(
                        f"{rows['firstname']}, \
                        {rows['telephone_number']}: {output}"
                    )
        else:
            id_users_prompt = f"""SELECT USERS.id_user,
                                  USERS.telephone_number,USERS.firstname
                                  FROM CHILDREN LEFT JOIN USERS ON
                                  USERS.id_user = CHILDREN.index_parent
                                  WHERE CHILDREN.age =
                                  {age_children_result.iloc[0]['age']}
                                  ORDER BY CHILDREN.name"""
            id_users_prompt_result = self.user_manager.execute_query(
                id_users_prompt)
            for iter, rows in id_users_prompt_result.iterrows():
                children_prompt = f"""SELECT CHILDREN.name, CHILDREN.age
                                      FROM CHILDREN LEFT JOIN USERS ON
                                      USERS.id_user = CHILDREN.index_parent
                                      WHERE {rows['id_user']} =
                                      CHILDREN.index_parent
                                      ORDER BY CHILDREN.name"""
                children_prompt_result = self.user_manager.execute_query(
                    children_prompt)
                output = "; ".join(
                    [
                        f"{row['name']}, {row['age']}"
                        for _, row in children_prompt_result.iterrows()
                    ]
                )
                console_output.append(
                    f"{rows['firstname']}, {rows['telephone_number']}: {output}"
                )
        return "\n".join(list(dict.fromkeys(console_output)))
