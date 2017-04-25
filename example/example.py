from pony_up import migrate
from pony import orm
import os

def bind_to_database(db):
    db.bind("postgres", host="posgres", user="some_user", password="1234secure", database="db1")
    db.generate_mapping(create_tables=True)
    # see methods in https://docs.ponyorm.com/api_reference.html?highlight=database#Database
# end def

# you can just use /path/to/examples/migrations instead of this `migrations_folder`
# this line is just to get it dynamically.
migrations_folder = os.path.join(os.path.pardir(os.path.abspath(__file__)), "migrations")

python_import = "migrations"  # Like in `from migrations import v0`

db = migrate(bind_to_database, folder_path=migrations_folder, python_import=python_import)

# Now use db as usual.

new_user1 = db.User(id=42, name_first="Max", name_last="Mustermann")
new_user2 = db.User(id=4458, name_first="John", name_last="Doe")

example_a = orm.select(u for u in db.User).limit(1)
print(example_a)
# [ User[42] ]

example_b = db.User.get(name_first="Max")
print(example_b)
# User[42]

example_c = db.User[4458]
print(example_c)
# User[4458]
