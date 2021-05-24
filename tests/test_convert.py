from picodoc import open_db
import unittest
from .config import TEST_DB_NAME


class TestConvert(unittest.TestCase):
    def setUp(self):
        self.db = open_db(TEST_DB_NAME)
        self.db['users'] = {}
        self.db['users']['donkere.v'] = {
            "name": "Donkere Vader",
            "private_field": "secret",
        }
        self.db['list'] = ["hello", "secret", "test"]

    def tearDown(self):
        self.db.reset()

    def test_dict_exclude(self):
        dct = self.db['users']['donkere.v'].to_dict(exclude=["private_field"])
        self.assertEqual(
            dct,
            {"name": "Donkere Vader"}
        )

    def test_list_exclude(self):
        lst = self.db['list'].to_dict(exclude=[1])
        self.assertEqual(
            lst,
            ["hello", "test"]
        )
