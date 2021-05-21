from .models import Document


def get_db():
    root = Document.select().where(Document.key_id == "root")
    if root.exists():
        root = root.get()
    else:
        root = Document(key_id="root", parent=None)
        root.save()
    return root
