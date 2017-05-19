from datetime import datetime
from pony import orm


def register_database(db, do_temp_table=False):
    """
    
    :param db: 
    :param do_temp_table: This is set to true, when v2 imports this, as temporary table to copy it. It will later rename it.
    :return: 
    """
    class Test(db.Entity):
        id = orm.PrimaryKey(int, auto=True)
        emoji = orm.Required(orm.unicode, index=True)
        text = orm.Optional(str, nullable=True)
        modified = orm.Required(datetime, sql_default="NOW()", volatile=True)
        user = orm.Required("User")

    class User(db.Entity):
        id = orm.PrimaryKey(int)
        name_first = orm.Optional(str, nullable=True)
        name_last = orm.Optional(str, nullable=True)
        tag = orm.Set("Tag")
        tests = orm.Set("Test")

    class Tag(db.Entity):
        id = orm.PrimaryKey(int, auto=True)
        user = orm.Required(User, column='user_id')
        message_id = orm.Optional(int)  # Of the message with the text, the tag. None means it got added via web gui.
        string = orm.Required(orm.unicode, index=True)

    if do_temp_table:
        setattr(Test, "_table_", "_pony_up__temp_" + Test.name)
        setattr(User, "_table_", "_pony_up__temp_" + User.name)
        setattr(Tag, "_table_", "_pony_up__temp_" + Tag.name)
