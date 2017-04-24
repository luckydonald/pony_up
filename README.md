# PonyUp!
Migrations for ponyorm

## Very simple migrations.

### Getting started

This is the first beta version, thus there is no installer yet.

Just add the `database_migrations/` folder to your project.

Set the database information, you have two ways to do that:

1. Create a `secret.py` with the variables `POSTGRES_HOST`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` set.

2. Edit `do_update.py`'s `def bind_database` (especially the `db.bind(...)` command)
 to have your sever information

The updates are applied as soon as `do_update.py` is imported, to expose `db` being the latest schema.

### File schema

- `migrations`
    - `v{number}`
        - `model`: model of version `{number}`
        - `migrate`: the script which updates from `{number}` to `{number+1}`