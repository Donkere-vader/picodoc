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
        self.db.drop_db()

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

    def test_same_key(self):
        self.db['test'] = {}
        self.db['test']['donkere.v'] = {
            "name": "wat"
        }
        self.assertEqual(self.db.to_dict(), {'users': {'donkere.v': {'name': 'Donkere Vader'}}, 'test': {'donkere.v': {'name': 'wat'}}})

    def test_set_to_doc(self):
        self.db['item'] = {'test': '123'}
        self.db['item2'] = self.db['item']
        self.assertEqual(self.db['item2'].to_dict(), self.db['item'].to_dict())
