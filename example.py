from picodb import get_db

db = get_db()

db['test'] = {
    "test": 123
}

db['wat'] = [1, 2, 3]
print(db)
print(db['wat'])
print(db['wat'][0])
