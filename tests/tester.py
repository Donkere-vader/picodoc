from re import DEBUG
from src.picodoc import open_db
import unittest
import os
import sys

TEST_DB_NAME = "picodb_temp_tests_database.db"


class StrTest(unittest.TestCase):
    def test_str(self):
        """
        Test if db can hold string values
        """
        self.assertEqual(1, 1)


def run_tests(keep_db=False, force_db_reset=False):
    if not force_db_reset and TEST_DB_NAME in os.listdir():
        if input(f"Database '{TEST_DB_NAME}' Already exists. Continuing will delete all data.\nDo you wish to continue? [Y/n] ").lower().strip() not in ["y", ""]:
            exit()

    global DB
    DB = open_db(TEST_DB_NAME)
    DB.reset()

    unittest.main(exit=False, argv=[sys.argv[0]])

    if TEST_DB_NAME in os.listdir() and not keep_db:
        os.remove(TEST_DB_NAME)
