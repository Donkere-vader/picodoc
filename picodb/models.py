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
            elif type(value) == List:
                value = value.get_value()
            obj[field.key] = value

        return obj

    @property
    def parent_doc(self):
        return self.parent.parent

    class Meta:
        database = db


class Item(Model):
    value = CharField(null=True)
    value_type = CharField(null=True)

    def get_value(self):
        print(self.value, type(self.value), self.value_type)
        if self.value_type == "str":
            return str(self.value)
        elif self.value_type == "int":
            return int(self.value)
        elif self.value_type == "bool":
            return True if self.value == "True" else False
        elif self.value_type == "doc":
            return Document.select().where(Document.id == self.value).get()
        elif self.value_type == "list":
            return List.select().where(List.id == self.value).get()

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

            self.value = str(new_doc.id)
        elif type(value) == list:
            self.value_type = "list"

            new_list = List(parent=self)
            new_list.save()

            for item in value:
                new_list.append(item)

            self.value = str(new_list.id)

        if type(value) in [str, int, bool]:
            self.value = str(value)

    class Meta:
        database = db


class Field(Item):
    parent = ForeignKeyField(Document, backref="fields")
    key = CharField()


class List(Model):
    parent = DeferredForeignKey("Field", backref="lists", null=True)

    def get_value(self):
        return [item.get_value() for item in self.items]

    def append(self, value):
        new_item = ListItem(parent=self)
        new_item.set_value(value)
        new_item.save()
        print("Value from object:", new_item.value)
        print("Value from queried object: ", ListItem.select().where(ListItem.id == new_item.id).get().value)

    def remove(self, value):
        for field in self.fields:
            if field.get_value() == value:
                field.delete_instance()
                return

    def __getitem__(self, idx):
        pass

    def __setitem__(self, idx, value):
        pass

    class Meta:
        database = db


class ListItem(Item):
    parent = ForeignKeyField(List, backref="items")
    value = CharField


db.connect()
db.create_tables([Document, Field, List, ListItem])
