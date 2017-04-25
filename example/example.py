from pony_up.do_update import do_all_migrations
from pony import orm

def bind_to_database(db):
    db.bind("postgres", host="posgres", user="some_user", password="1234secure", database="db1")
    db.generate_mapping(create_tables=True)

import os

# you can just use /path/to/examples/migrations instead of this `migrations_folder`
# this line is just to get it dynamically.
migrations_folder = os.path.join(os.path.pardir(os.path.abspath(__file__)), "migrations")

python_import = "migrations"  # Like in `from migrations import v0`

db = do_all_migrations(bind_to_database, folder_path=migrations_folder, python_import=python_import)

# Now use db as usual.

new_user1 = db.User(id=42, name_first="Max", name_last="Mustermann")
new_user2 = db.User(id=4458, name_first="John", name_last="Doe")

example = orm.select(u for u in db.User).limit(1)
print(example[0])
# User[42]