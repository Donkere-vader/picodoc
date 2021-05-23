from picodoc import open_db
import unittest
from .config import TEST_DB_NAME


class TestList(unittest.TestCase):
    def setUp(self):
        self.db = open_db(TEST_DB_NAME)
        self.db['numbers'] = [0, 1, 2, 3]

    def tearDown(self):
        self.db.reset()

    def test_del_idx(self):
        del self.db['numbers'][0]
        self.assertEqual(self.db['numbers'].to_dict(), [1, 2, 3])

    def test_remove(self):
        self.db['numbers'].remove(1)
        self.assertEqual(self.db['numbers'].to_dict(), [0, 2, 3])

    def test_append(self):
        self.db['numbers'].append(4)
        self.assertEqual(self.db['numbers'].to_dict(), [0, 1, 2, 3, 4])

    def test_iter(self):
        values = [value for value in self.db['numbers']]
        self.assertEqual(values, [0, 1, 2, 3])

    def test_overwrite(self):
        self.db['numbers'][0] = 1
        self.assertEqual(self.db['numbers'].to_dict(), [1, 1, 2, 3])
