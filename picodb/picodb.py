from .models import Document


def get_db():
    root = Document.select().where(Document.root)
    if root.exists():
        root = root.get()
    else:
        root = Document(root=True, parent=None)
        root.save()
    return root
