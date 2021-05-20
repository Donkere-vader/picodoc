from picodb import get_db

db = get_db()

db['test'] = {
    "test": 123
}

db['wat'] = 'test'

test_doc = db['test']
print(test_doc.parent_doc)

print(db)
