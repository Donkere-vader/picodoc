from picodb import PicoDb

db = PicoDb("database.json", indent=4)

db['users'] = {}

db['users']['user_id'] = {
    "username": "Example_username",
    "email": "me@example.com",
}

db.commit()

print(db)
