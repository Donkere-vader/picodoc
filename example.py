from picodb import get_db
from rich import print

db = get_db()

db['test'] = {
    "test": 123,
    "tast": False
}

db['wat'] = [1, 2, 3]
print(db)
print(db['test'])
print(db['test']['test'])
# print(db['wat'][0])
