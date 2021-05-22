from picodb import open_db
from rich import print
import os


TEST_DB_NAME = "picodb_temp_tests_database.db"


####################
# EXCEPTIONS
####################

class UnexpectedResult(Exception):
    pass

####################
# TEST
####################

def str_test():
    db = open_db(TEST_DB_NAME)
    db['value'] = "123"
    return db.to_dict()


def int_test():
    db = open_db(TEST_DB_NAME)
    db['value'] = 123
    return db.to_dict()


def float_test():
    db = open_db(TEST_DB_NAME)
    db['value'] = 123.1
    return db.to_dict()


def bool_test():
    db = open_db(TEST_DB_NAME)
    db['value'] = False
    return db.to_dict()


def list_test():
    db = open_db(TEST_DB_NAME)
    db['value'] = [1, 2, 3]
    db['value'][0] = 0
    db['value'].append(4)
    return db.to_dict()


def iter_test():
    db = open_db(TEST_DB_NAME)
    db['value'] = [0, 1, 2]
    obj = {
        "list": [],
        "dict": {}
    }
    for item in db['value']:
        obj['list'].append(item + 1)
    db['value2'] = {'test': 0, 'test1': 1}
    for key in db['value2']:
        obj['dict'][key] = db['value2'][key] + 1
    return obj


def nested_test():
    db = open_db(TEST_DB_NAME)

    db['posts'] = {}
    db['users'] = {}
    db['users']['donkere.v'] = "That's me!"
    return db.to_dict()


tests = [
    {
        "test": str_test,
        "expected_result": {
            "value": "123"
        },
    },
    {
        "test": int_test,
        "expected_result": {
            "value": 123,
        },
    },
    {
        "test": float_test,
        "expected_result": {
            "value": 123.1,
        },
    },
    {
        "test": bool_test,
        "expected_result": {
            "value": False,
        },
    },
    {
        "test": list_test,
        "expected_result": {
            "value": [0, 2, 3, 4],
        },
    },
    {
        "test": iter_test,
        "expected_result": {
            "list": [1, 2, 3],
            "dict": {
                'test': 1,
                'test1': 2,
            }
        }
    },
    {
        "test": nested_test,
        "expected_result": {
            "posts": {},
            "users": {
                "donkere.v": "That's me!"
            },
        },
    },
]

####################
# RUN TESTS
####################

results = {}

def main():
    if TEST_DB_NAME in os.listdir():
        print(f"'{TEST_DB_NAME}' already exists. Continuing will delete it.\nAre you sure you want to continue? [Y/n] ", end="")
        if input().lower() not in ["", "Y"]:
            exit()
        os.remove(TEST_DB_NAME)
        print()

    print("Running tests...\n")

    for test_dict in tests:
        test = test_dict['test']
        try:
            outcome = test()
            if str(outcome) != str(test_dict['expected_result']):  # yes converting to str is nessacerry for some reason. Otherwise I'll have to deal with pointer and instance bs.
                raise UnexpectedResult(f"Expected {test_dict['expected_result']} but encountered {outcome}")
            results[test.__name__] = {
                "succes": True
            }
            print(f"[bold green]\t✅ Test '{test.__name__}' completed succesfully[/bold green]")
        except Exception as e:
            results[test.__name__] = {
                "succes": False,
                "error": e
            }
            print(f"[bold red]\t❌ Test '{test.__name__}' failed[/bold red]\n\t\t{e}\n\t\tln: {e.__traceback__.tb_lineno}")

        if TEST_DB_NAME in os.listdir():
            os.remove(TEST_DB_NAME)

if __name__ == "__main__":
    main()
