import random
from string import ascii_letters

characters = list(ascii_letters) + [str(i) for i in range(10)]


def create_id(name=None, length=20):
    if name is None:
        name = ""
    name = name.lower().replace(" ", "_")
    return ((name + "-") if name else "") + "".join([random.choice(characters) for _ in range(length - len(name) - (1 if name else 0))])
