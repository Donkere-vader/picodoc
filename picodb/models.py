from peewee import BooleanField, ForeignKeyField, IntegerField, Model, SqliteDatabase, CharField, DeferredForeignKey
from .config import SUPPORTED_TYPES
import json


db = SqliteDatabase('database.sqlite')


class Document(Model):
    key_id = CharField()
    parent = ForeignKeyField('self', backref='documents', null=True)
    str_value = CharField(null=True)
    value_type = CharField(default="dict")

    class Meta:
        database = db

    @property
    def value(self):
        for tpe in [int, str, float]:
            if self.value_type == tpe.__name__:
                return tpe(self.str_value)
        if self.value_type == bool.__name__:
            return True if self.str_value == "True" else False

    def __setitem__(self, key, value):
        del self[key]

        value_type = str(type(value).__name__)
        if value_type not in SUPPORTED_TYPES:
            raise ValueError(f"'{value_type}' is not one of the supported types: {' '.join(SUPPORTED_TYPES)}")
        str_value = None
        if type(value) in [int, str, float, bool]:
            str_value = str(value)

        new_doc = Document(key_id=key, parent=self, str_value=str_value, value_type=value_type)
        new_doc.save()

        if value_type == "dict":
            for key in value:
                new_doc[key] = value[key]

    def __getitem__(self, key):
        query = self.select().where(Document.key_id == key and Document.parent == self)
        if not query.exists():
            raise KeyError(f"Document {self.object_repr()} does not contain key '{key}'")
        doc = query.get()
        return doc if doc.value_type == "dict" else doc.value

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return json.dumps(self.to_dict(), indent=4)

    def to_dict(self):
        if self.value_type == "dict":
            obj = {}
            for doc in self.documents:
                obj[doc.key_id] = doc.to_dict()
        elif self.value_type == "list":
            obj = "list...placeholder"
        else:
            return self.value

        return obj

    def object_repr(self) -> str:
        return f"<Document {self.key_id} {self.id}>"

    def __delitem__(self, key):
        self.delete().where(Document.key_id == key and Document.parent == self)


# class Value(Model):

#     def set_value(self, value):
#         pass

#     def get_value(self):
#         if self.value_type == "str":
#             return self.str_value
#         elif self.value_type == "int":
#             return int(self.str_value)
#         elif self.value_type == "float":
#             return float(self.str_value)
#         elif self.value_type == "bool":
#             return True if self.str_value == "True" else False
#         elif self.value_type == "doc":
#             return Document.select().where(Document.id == int(self.str_value)).get()

#     @property
#     def value(self):
#         return self.get_value()

#     def __setattr__(self, name, value) -> None:
#         if name == "value":
#             self.set_value(value)
#             return
#         return super().__setattr__(name, value)

db.connect()
db.create_tables([Document])
