# PicoDoc 📝

This is a document database module made for small-scale applications. Please don't use this module if your data is very important. It is not tested very extensively.

This project is on [pypi](https://pypi.org/project/picodoc/) and on [github](https://www.github.com/donkere-vader/picodb).

## Installation

The project is up on pypi (PYthon Package Index). So installing can be done using ``pip``.

Unix & Mac os X:

```sh
pip3 install picodoc
```

Windows:

```cmd
pip install picodoc
```

## ⚠ Notice

The objects are not really dicts and lists. So they do not support all functions of those objects.

List supports:

- [X] append
- [X] remove
- [x] iterating over values
- [X] item assignment using index
  - [X] ``del list[idx]``
  - [X] ``value = list[idx]``
  - [X] ``list[idx] = new_value``

Dict supports:

- [x] iterating over keys
- [X] item assignment using key
  - [X] ``del list[key]``
  - [X] ``value = list[key]``
  - [X] ``list[key] = new_value``

## Usage

Using the library should be very straight forward. Open a database with the ``picodoc.open_db`` function and use it as if it were a dict.

To get started import the module

```py
import picodoc
```

Then open the database. (The extension doesn't really matter, but I would suggest using something lile '.db' or '.picodoc')

```py
db = picodoc.open_db('database.picodoc')
```

Now just treat the db as af it were a basic (see [notice](#⚠_notice)) dictionary.

```py
db['users'] = {}
db['users']['donkere.v'] = {
    'name':  'Donkere Vader',
    'descprition': 'Cool dude 😎',
}
```

There are two ways of printing a document.

Either print it as a dict:

```py
print(db['users']['donkere.v'])

>>>
<Document donkere.v>
{
    'name':  'Donkere Vader',
    'descprition': 'Cool dude 😎',
}
```

Or print it as an object:

```py
# this will print it as if it were a document
# <Document {document key}>
print(db['users']['donkere.v'].object_repr())

>>>
<Document donkere.v>
```

### Tip

Use the [rich module](https://github.com/willmcgugan/rich) for beautiful output in the console.

## Testing

Testing is done via the ``runtests`` file.

To run all the tests simply do:

```sh
python3 runtests
```

(If you are on windows use ``python`` in stead of ``python3``)
