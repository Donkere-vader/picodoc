import json
import os


class PicoDb:
    def __init__(self, database_name, indent=None):
        self.db_name = database_name
        self.indent = indent
        self.db_file = self.open_file()

        self.json_obj = self.load(self.db_file)

    def open_file(self):
        files = os.listdir()

        if self.db_name not in files:
            with open(self.db_name, "w") as f:
                f.write(json.dumps({}))

        return open(self.db_name, 'r')

    def load(self, *args, **kwargs):
        return json.load(*args, **kwargs)

    def loads(self, *args, **kwargs):
        return json.loads(*args, **kwargs)

    def commit(self):
        with open(self.db_name, "w") as f:
            f.write(json.dumps(self.json_obj, indent=self.indent))

    def __getitem__(self, key):
        return self.json_obj[key]

    def __setitem__(self, key, value):
        self.json_obj[key] = value

    def __repr__(self) -> str:
        return f"<PicoDb '{self.db_name}'>"
