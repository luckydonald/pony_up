from pony import orm


def do_update(db, old_db=None):
    print(("do_update:", db, old_db))
    assert isinstance(db, orm.Database)
    db.execute(
        "ALTER TABLE test ADD COLUMN modified "
        "TIMESTAMP NOT NULL DEFAULT NOW()", dict())
    db.execute(
        "CREATE OR REPLACE FUNCTION update_modified_column() "
        "RETURNS TRIGGER AS $$$$ "
        "BEGIN "
        "    NEW.modified = now(); "
        "    RETURN NEW; "
        "END; "
        "$$$$ language 'plpgsql';", dict())
    db.execute(
        "DROP TRIGGER IF EXISTS update_test_modified ON test;", dict())
    db.execute(
        "CREATE TRIGGER update_test_modified BEFORE UPDATE ON test "
        "FOR EACH ROW EXECUTE PROCEDURE update_modified_column();", dict())
    orm.commit()
    return (1, {"message": "Added `update_test_modified` Trigger, for `test.modified`."})
# end def


def register_migration():
    return 0, do_update
# end def