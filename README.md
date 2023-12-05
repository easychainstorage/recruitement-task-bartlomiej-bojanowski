# recruitement-task-bartlomiej-bojanowski

## Installation
First you need to install packages
```
pip3 install -r requirements.txt
```
## Create database 
To use script you need first create database
```python
python script.py create_database
```

## Usage
All commands bellow require two arguments
```bash
--login          Email or telephone number
--password       Password to account.
```

### Only admin role accounts
- **Print The Number of All Valid Accounts**

Print the total number of valid accounts.
```bash
python script.py print-all-accounts --login xyz --password xyz
```
- **Print The Longest Existing Account**

Print information about the account with the longest existence.
```bash
python script.py print-oldest-account --login xyz --password xyz
```

- **Group Children by Age**

Print group children by age and display relevant information.
```bash
python script.py group-by-age --login xyz --password xyz
```
### Admin and user role accounts
- **Print Children**

Display information about the user's children.
```bash
python script.py print-children --login xyz --password xyz
```

- **Find Users with Children of Same Age**

Find users with children of the same age as at least one own child, print the user and all of his children data
```bash
python script.py find-similar-children-by-age --login xyz --password xyz
```

## Test
To run tests
```bash
python -m unittest
```