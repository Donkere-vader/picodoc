from peewee import BooleanField, ForeignKeyField, IntegerField, Model, SqliteDatabase, CharField, DeferredForeignKey
from .config import SUPPORTED_TYPES
import json


db = SqliteDatabase(None)


class Document(Model):
    key_id = CharField()
    parent = ForeignKeyField('self', backref='documents', null=True)
    str_value = CharField(null=True)
    value_type = CharField(default=dict.__name__)

    class Meta:
        database = db

    @property
    def value(self):
        for tpe in [int, str, float]:
            if self.value_type == tpe.__name__:
                return tpe(self.str_value)
        if self.value_type == bool.__name__:
            return True if self.str_value == "True" else False

    def __setitem__(self, key, value, force_insert=False):
        if self.value_type == list.__name__ and key > Document.select().where(Document.parent == self).count() and not force_insert:
            raise IndexError(f"Index {key} out of bounds")
        del self[key]

        value_type = str(type(value).__name__)
        if value_type not in SUPPORTED_TYPES:
            raise ValueError(f"'{value_type}' is not one of the supported types: {' '.join(SUPPORTED_TYPES)}")
        str_value = None
        if type(value) in [int, str, float, bool]:
            str_value = str(value)

        new_doc = Document(key_id=key, parent=self, str_value=str_value, value_type=value_type)
        new_doc.save()

        if value_type == dict.__name__:
            for key in value:
                new_doc[key] = value[key]
        elif value_type == list.__name__:
            for idx, item in enumerate(value):
                new_doc[idx] = item

    def append(self, item):
        if self.value_type != list.__name__:
            raise TypeError(f"'{self.value_type}' has no attribute append")
        length = Document.select().where(Document.parent == self).count()
        self.__setitem__(length, item, force_insert=True)

    def remove(self, idx):
        if self.value_type != list.__name__:
            raise TypeError(f"'{self.value_type}' has no attribute append")

        del self[idx]

    def __getitem__(self, key):
        query = self.select().where((Document.key_id == key) & (Document.parent == self))
        if not query.exists():
            raise KeyError(f"Document {self.object_repr()} does not contain key '{key}'")
        doc = query.get()
        return doc if doc.value_type in [dict.__name__, list.__name__] else doc.value

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return json.dumps(self.to_dict(), indent=4)

    def __delitem__(self, key):
        self.delete().where((Document.key_id == key) & (Document.parent == self)).execute()

    def reset(self):
        for doc in self.documents:
            doc.delete_instance()

    def __iter__(self):
        if self.value_type not in [dict.__name__, list.__name__]:
            raise TypeError(f"'{self.value_type}' is not iterable ")

        for doc in self.documents:
            yield doc.value if self.value_type == list.__name__ else doc.key_id

    def to_dict(self):
        if self.value_type == dict.__name__:
            obj = {}
            for doc in self.documents:
                obj[doc.key_id] = doc.to_dict()
        elif self.value_type == list.__name__:
            obj = [None for _ in range(Document.select().where(Document.parent == self).count())]
            for doc in self.documents:
                obj[int(doc.key_id)] = doc
        else:
            return self.value

        return obj

    def object_repr(self) -> str:
        return f"<Document {self.key_id} {self.id}>"
