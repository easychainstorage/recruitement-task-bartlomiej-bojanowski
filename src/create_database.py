import os
import re
import sqlite3
import xml.etree.ElementTree as ET

import pandas as pd


class LoadData:
    """
    A class for loading and processing data from different file formats.
    """
    def __init__(self, directory):
        """
        Initializes the LoadData class with a list of files
        from the specified directory.

        :param directory: The path to the directory containing data files.
        """
        self.list_of_files = self.list_documents_in_directory(directory)

    @staticmethod
    def read_xml(file):
        tree = ET.parse(file)
        root = tree.getroot()
        list_dict = []

        for user in root.findall(".//user"):
            children_list = []
            row_dict = {
                u.tag: u.text
                for u in user.iter()
                if u.tag not in ["user", "age", "name", "child"]
            }
            children = user.find(".//children")
            row_dict["children"] = [
                child.attrib for child in children.findall(".//child")
            ]
            for child in children.findall(".//child"):
                child_dict = dict()
                for c in child:
                    child_dict[c.tag] = c.text
                children_list.append(child_dict)
                row_dict["children"] = children_list
            list_dict.append(row_dict)
        return list_dict

    @staticmethod
    def list_documents_in_directory(directory):
        return [
            os.path.join(root, file)
            for root, _, files in os.walk(directory)
            for file in files
        ]

    def concat_data(self):
        df = pd.DataFrame()
        for file in self.list_of_files:
            if file.endswith(".csv"):
                df_file = pd.read_csv(file, delimiter=";")
            elif file.endswith(".json"):
                df_file = pd.read_json(file)
            elif file.endswith(".xml"):
                df_file = pd.DataFrame(self.read_xml(file))
            df = pd.concat([df, df_file], ignore_index=True)
        return df


class Users:
    """
    A class for processing user data.
    """
    def __init__(self, data):
        """
        Initializes the Users class with user data.

        :param data: A pandas DataFrame containing user data.
        """
        self.data = data

    @staticmethod
    def valid_telephone(number):
        pattern = r"^\+48|^48|^\(48\)|^00"
        number = re.sub(pattern, "", number)
        return number.replace(" ", "")

    def process_user_data(self):
        self.remove_nan()
        self.validate_email()
        self.format_telephone()
        self.format_creation_date()
        self.data = self.data.sort_values(
            by=["created_at"], ascending=False
        ).drop_duplicates(subset=["email"], keep="last")
        self.data = self.data.drop_duplicates(subset=["telephone_number"],
                                              keep="last")
        self.data.index.names = ["id_user"]

    def validate_email(self):
        pattern = r"^[^@]+@[^@\.]+\.[a-zA-Z0-9]{1,4}$"
        self.data = self.data[self.data["email"].str.contains(pattern)]

    def format_telephone(self):
        self.data["telephone_number"] = self.data["telephone_number"].map(
            self.valid_telephone
        )

    def format_creation_date(self):
        self.data["created_at"] = self.data["created_at"].map(str)

    def remove_nan(self):
        self.data = self.data[self.data["telephone_number"].notna()]


class Children:
    """
    A class for processing children data associated with users.
    """
    def __init__(self, user_data):
        """
        Initializes the Children class with user data.

        :param user_data: A pandas DataFrame containing user data,
        including children information.
        """
        self.user_data = user_data

    def process_children_data(self):
        children_database = []
        for index, row in self.user_data.iterrows():
            if row["children"]:
                children_database.extend(
                    self.process_individual_child(row["children"], index)
                )
        return pd.DataFrame(children_database)

    def process_individual_child(self, children, parent_index):
        processed_children = []
        if isinstance(children, list):
            for child in children:
                child["index_parent"] = parent_index
                processed_children.append(child)
        elif not pd.isna(children):
            for child in children.split(","):
                child_data = {
                    "name": child.split(" ")[0],
                    "index_parent": parent_index,
                    "age": re.search(r"\d{1,2}", child).group(),
                }
                processed_children.append(child_data)
        return processed_children


class DatabaseManager:
    """
    A class for managing database operations.
    """
    def __init__(self, db_name="users.sqlite3"):
        """
        Initializes the DatabaseManager with a SQLite database connection.

        :param db_name: The name of the SQLite database file.
        Default is 'users.sqlite3'.
        """
        self.conn = sqlite3.connect(db_name)

    def save_to_database(self, df, table_name):
        df.to_sql(name=table_name, con=self.conn)

    def close_connection(self):
        self.conn.close()


def create_database(args):
    """
    A function to create and populate a database with user and children data.

    This function reads data from files, processes it, and saves it into a
    SQLite database.

    :param args: Arguments for database creation (currently not used).
    """
    db_manager = DatabaseManager()
    df_concat = LoadData("data").concat_data()
    user_processor = Users(df_concat)
    user_processor.process_user_data()

    children_processor = Children(user_processor.data)
    children_df = children_processor.process_children_data()
    db_manager.save_to_database(children_df, "Children")

    db_manager.save_to_database(user_processor.data.drop(
        columns=["children"]), "Users")

    db_manager.close_connection()
