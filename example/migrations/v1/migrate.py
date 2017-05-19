from datetime import datetime
from pony import orm
from pony_up import Migrator


def do_update(migrator):
    assert isinstance(migrator, Migrator)
    print(migrator)
    print(str(migrator))
    assert migrator.new_db
    db = migrator.new_db
    db.execute('ALTER TABLE "test"  ADD COLUMN "user" INTEGER;')
    db.execute('ALTER TABLE "test" ADD CONSTRAINT "fk_test__user" FOREIGN KEY ("user") REFERENCES "user" ("id");')
    return 2, {"message": "Added `modified` column, to `test` table."}
