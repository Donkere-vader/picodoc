from src.picodoc import open_db
import unittest
import os
from .config import TEST_DB_NAME


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = open_db(TEST_DB_NAME)

    def test_str(self):
        self.assertEqual(1, 1)

    def test_int(self):
        self.assertEqual('test', 'test')

    def tearDown(self):
        self.db.reset()
