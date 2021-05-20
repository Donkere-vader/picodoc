from peewee import BooleanField, ForeignKeyField, Model, SqliteDatabase, CharField, DeferredForeignKey
import json


db = SqliteDatabase('database.sqlite')


class Document(Model):
    root = BooleanField(default=False)
    parent = DeferredForeignKey("Field", backref="documents", null=True)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)

    def __getitem__(self, key):
        field = self.fields.select().where(Field.key == key)
        if not field.exists():
            return None
        return field.get().get_value()

    def __setitem__(self, key, value):
        field = self.fields.select().where(Field.key == key)
        if not field.exists():
            field = Field(parent=self, key=key, value=None, value_type=None)
        else:
            field = field.get()
        field.set_value(value)
        field.save()

    def __delitem__(self, key):
        field = self.fields.select().where(Field.key == key)
        if not field.exists():
            return
        else:
            field = field.get()
            field.delete_instance()

    def to_dict(self):
        obj = {}

        for field in self.fields:
            value = field.get_value()
            if type(value) == Document:
                value = value.to_dict()
            obj[field.key] = value

        return obj

    @property
    def parent_doc(self):
        return self.parent.parent

    class Meta:
        database = db


class Field(Model):
    parent = ForeignKeyField(Document, backref="fields")
    key = CharField()
    value = CharField(null=True)
    value_type = CharField(null=True)

    def get_value(self):
        if self.value_type == "str":
            return str(self.value)
        elif self.value_type == "int":
            return int(self.value)
        elif self.value_type == "bool":
            return True if self.value == "True" else False
        elif self.value_type == "doc":
            return Document.select().where(Document.id == self.value).get()

    def set_value(self, value):

        if self.value_type == "doc":
            Document.delete().where(Document.id == self.value).execute()

        if type(value) == str:
            self.value_type = "str"
        elif type(value) == int:
            self.value_type = "int"
        elif type(value) == bool:
            self.value_type = "bool"
        elif type(value) == dict:
            self.value_type = "doc"

            new_doc = Document(parent=self)
            new_doc.save()
            for key in value:
                new_doc[key] = value[key]

            self.value = new_doc.id

        if type(value) in [str, int, bool]:
            self.value = str(value)

    class Meta:
        database = db


db.connect()
db.create_tables([Document, Field])
