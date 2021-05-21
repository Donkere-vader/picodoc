# PicoDb

Just a very simple Python dict/ JSON database. Not safe. Don't use if your data is important.


## Usage

Using the library should be very straight forward. Open a database with the ``picodb.open_db`` function and use it as if it were a dict.

```py
import picodb

db = picodb.open_db("database.picodb")  # It's a sqlite database under the hood

# db is now your root of the document database

db['users'] = {}
db['users']['john.doe'] = {
    "name": "John Doe",
    "email": "john.doe@example.com",
}

# saving is done automatically

print(db)

>>>

{
    "users": {
        "john.doe": {
            "name": "John Doe",
            "email": "john.doe@example.com"
        }
    }
}
```
