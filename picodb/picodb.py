from .models import Document, db


def open_db(database_name):
    db.init(database_name)
    db.connect()
    db.create_tables([Document])

    root = Document.select().where(Document.key_id == "root")
    if root.exists():
        root = root.get()
    else:
        root = Document(key_id="root", parent=None)
        root.save()
    return root
