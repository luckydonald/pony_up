from datetime import datetime
from pony import orm
from pony_up import Migrator


def do_update(migrator):
    assert isinstance(migrator, Migrator)
    assert migrator.old_db
    db = migrator.old_db
    assert migrator.new_db
    _table_ = "temp_test"

    return 4, {"message": "Added `user` column, to `test` table."}
