# PonyUp!
###### Version `0.1.1`
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
    db.bind('database type', host='localhost', user='root', passwd='1234secure', db='test1')
    # https://docs.ponyorm.com/api_reference.html#Database.bind
    db.generate_mapping(create_tables=True)
    # https://docs.ponyorm.com/api_reference.html#Database.generate_mapping
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

### Info graphic
![migrations](https://cloud.githubusercontent.com/assets/2737108/25397889/3a75eca2-29ea-11e7-9527-0bb3cc1412ef.png)    
_Fig 1. Migrations_

### FAQ
##### How to use
> See above, or have a look at the example.

##### Can I contribute?
> Please do!    
> Report issues, suggest features, or even submit code!

##### I don't like using `db.{EntityName}`.
I have used the file `database.py` before, to include all my objects,
and still like to use the existing import statements. I imported:
```python
from database import {EntityName}
```
or even import all the database entities with the wildcard import
```python
from database import *
```

> You should move the entity definitions in `database.py` into a migrations step (`v0.model` perhaps),
> and replace the file content with `db = migrate(...)`, like seen above.    
> Now you can add the following lines after said `db = migrate(...)` part:    
> ```python
> # register the tables to this module
> __all__ = ["db"]
> for t_name, t_clazz in db.entities.items():
>     globals()[t_name] = t_clazz
>     __all__.append(t_name)
> # end for
> ```

##### Where does the name come from?
> Because of the library `Pony ORM`, the verb `to pony up` and this tool doing `updates`!    
> Got it? Yeah, what a sick joke! Tell your Grandma, too!

##### Who is best pony?
> Definitely **Littlepip**! (see [Fallout: Equestria](http://falloutequestria.wikia.com/wiki/Fallout:_Equestria))

##### Why is this FAQ getting stupid now?
> lel.