from datetime import datetime
from pony import orm
from pony_up import Migrator


def do_update(migrator):
    assert isinstance(migrator, Migrator)
    db = migrator.new_db or migrator.old_db  # which ever is not None.
    assert db

    # create a temporary database
    temp_db = orm.Database()
    from ..v3 import model as model_v3
    model_v3.register_database(temp_db)
    migrator.bind_database_function(model_v3)

    db.execute()


    # update trigger (modified)
    return 3, {"message": "Added `user` column, to `test` table."}
