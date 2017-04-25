# PonyUp!
Migrations for ponyorm

## Very simple migrations.

### Getting started

This is the first beta version, thus there is <a title="littlepip is best pony" name="pip">pip</a> no installer yet.

Just add the `database_migrations/` folder to your project.

Set the database information, you have two ways to do that:

1. Create a `secret.py` with the variables `POSTGRES_HOST`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` set.

2. Edit `do_update.py`'s `def bind_database` (especially the `db.bind(...)` command)
 to have your sever information

3. `from pony_up.do_update import db`

The updates are applied as soon as `do_update.py` is imported, to expose `db` being the latest schema.

### File schema
- `pony_up`
    - `migrations`: The migrations are in here
        - `v{number}`: for example "v0"
            - `__init__.py`: needs to import the model and also migrate if present.
            - `model.py`: model of version `{number}`
            - `migrate.py`: the script which updates from `{number}` to `{number+1}`