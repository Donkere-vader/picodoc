from picodoc import open_db
import unittest
from .config import TEST_DB_NAME


class TestSetting(unittest.TestCase):
    def setUp(self):
        self.db = open_db(TEST_DB_NAME)

    def tearDown(self):
        self.db.reset()

    def test_set_to_string(self):
        self.db['test'] = "str"
        self.assertEqual(self.db['test'], "str")

    def test_set_to_int(self):
        self.db['test'] = 123
        self.assertEqual(self.db['test'], 123)

    def test_set_to_float(self):
        self.db['test'] = 123.1
        self.assertEqual(self.db['test'], 123.1)

    def test_set_to_bool(self):
        self.db['test'] = True
        self.assertEqual(self.db['test'], True)

    def test_set_to_dict(self):
        self.db['test'] = {}
        self.assertEqual(self.db['test'].to_dict(), {})

    def test_set_to_list(self):
        self.db['test'] = []
        self.assertEqual(self.db['test'].to_dict(), [])
