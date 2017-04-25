# PonyUp!
Migrations for ponyorm

## Very simple migrations.

### Install

This still a first beta version, but you can test it already with the following shell command:
```sh
$ pip install pony_up
```

### Getting started

```python
from pony_up import migrate

# to be able to bind the database with your information,
# just create a function for it:
def bind_func(db):
    db.bind("database type", "host", "user", "password", "database name")
    db.generate_mappings()
# end def


db = migrate(bind_func, folder_path="examples/migrations, python_import="examples.migrations")
```

The updates are applied as soon as `migrate` is called. It will return `db`, being the latest schema.

### Your File schema
- `migrations/`: The migrations are in here
    - `v{number}/`: for example "v0"
        - `__init__.py`: needs to import the model and also migrate if present.
        - `model.py`: model of version `{number}`
        - `migrate.py`: the script which updates from `{number}` to `{number+1}`
    - `v{number}.py`:
        A file is possible too, if it has the attribute `model` with a function `register_database` (calling `model.register_database(db)`)
        and optionally a `migrate` attribute with function `do_update` (will call `migrate.do_update(db)`)