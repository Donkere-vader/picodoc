from picodoc import open_db
import unittest
from .config import TEST_DB_NAME


class TestDict(unittest.TestCase):
    def setUp(self):
        self.db = open_db(TEST_DB_NAME)
        self.db['users'] = {}
        self.db['users']['donkere.v'] = {
            "name": "Donkere Vader"
        }

    def tearDown(self):
        self.db.reset()

    def test_del_key(self):
        del self.db['users']['donkere.v']
        self.assertEqual(self.db.to_dict(), {
            "users": {},
        })

    def test_overwrite_key(self):
        self.db['users']['donkere.v']['name'] = "Donkere Vader2"
        self.assertEqual(self.db['users']['donkere.v']['name'], "Donkere Vader2")

    def test_iter(self):
        keys = [key for key in self.db['users']]
        self.assertEqual(keys, ["donkere.v"])
