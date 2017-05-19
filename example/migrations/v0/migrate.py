from pony import orm

from pony_up import Migrator


def do_update(migrator):
    assert isinstance(migrator, Migrator)
    print(("do_update:", migrator))
    db = migrator.new_db
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

    # add some test data
    db.Test(emoji="😄", text="text")
    db.Test(emoji="😜", text="foobar")
    db.Test(emoji="😭")
    db.User(id=1, name_first="Max", name_last="Musterman")
    db.User(id=2, name_first="Jane", name_last="Doe")
    db.User(id=3, name_first="Otto", name_last="Normalverbraucher")
    u1 = db.User(id=4, name_first="Littlepip")
    db.Tag(user=u1, string="best pony", message_id=12)
    db.Tag(user=u1, string="Fallout Equestria")
    orm.commit()
    return (1, {"message": "Added `update_test_modified` Trigger, for `test.modified`."})
# end def
