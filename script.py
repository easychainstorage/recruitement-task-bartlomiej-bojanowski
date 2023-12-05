import argparse

from src.account_actions import AccountActions
from src.database_manager import DatabaseManager
from src.user_manager import UserManager
from src.create_database import create_database


def main():
    """
    Main function to run the command for users.
    """
    db_manager = DatabaseManager(database_name="users.sqlite3")
    user_manager = UserManager(db_manager)
    account_actions = AccountActions(user_manager)

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument(
        "--login", required=True, help="Email or telephone number."
    )
    parent_parser.add_argument(
        "--password", required=True, help="Password to account."
    )

    parser = argparse.ArgumentParser(add_help=False)
    subparsers = parser.add_subparsers()

    parser_create_database = subparsers.add_parser(
        "create_database",
        help="Create database from data folder.")
    parser_create_database.set_defaults(func=create_database)

    parser_all_accounts = subparsers.add_parser(
        "print-all-accounts", parents=[parent_parser],
        help="Print the total number of valid accounts."
    )
    parser_all_accounts.set_defaults(func=account_actions.print_all_accounts)

    parser_oldest_accounts = subparsers.add_parser(
        "print-oldest-account", parents=[parent_parser],
        help="Print information about the account "
             "with the longest existence."
    )
    parser_oldest_accounts.set_defaults(
        func=account_actions.print_oldest_account
    )
    parser_group_by_age = subparsers.add_parser(
        "group-by-age", parents=[parent_parser],
        help="Print group children by age and "
             "display relevant information."
    )
    parser_group_by_age.set_defaults(func=account_actions.group_by_age)

    parser_print_children = subparsers.add_parser(
        "print-children", parents=[parent_parser],
        help="Print information about your own children."
    )
    parser_print_children.set_defaults(func=account_actions.print_children)

    parser_find_similar_children_by_age = subparsers.add_parser(
        "find-similar-children-by-age", parents=[parent_parser],
        help="print users with children of the"
             "same age as at least one own child."
    )
    parser_find_similar_children_by_age.set_defaults(
        func=account_actions.find_similar_children_by_age
    )
    args = parser.parse_args()

    if hasattr(args, 'func'):
        print(args.func(vars(args)))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
