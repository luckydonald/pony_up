from luckydonaldUtils.logger import logging
from pony_up import migrate
from pony import orm
import os

logger = logging.getLogger(__name__)
logging.add_colored_handler(level=logging.DEBUG)


def bind_to_database(db):
    db.bind("postgres", user='postgres', port=5433, password='', host='localhost', database='postgres')
    db.generate_mapping(create_tables=True)
    # see methods in https://docs.ponyorm.com/api_reference.html?highlight=database#Database
# end def


# you can just use /path/to/examples/migrations instead of this `migrations_folder`
# this line is just to get it dynamically.
migrations_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "migrations")

python_import = "migrations"  # Like in `from migrations import v0`
orm.debug = True
try:
    db = migrate(bind_to_database, folder_path=migrations_folder, python_import=python_import)
except Exception as e:
    from time import sleep
    logger.exception("migration")
    sleep(2)  # to have some time between logging it and crashing.
    raise e
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
