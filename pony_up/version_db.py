from datetime import datetime
from pony import orm


def register_database(db):
    class Version(db.Entity):
        version = orm.PrimaryKey(int, auto=False)
        upgraded = orm.Required(datetime, sql_default='NOW()')
        meta = orm.Optional(orm.Json, lazy=True)
    # end class
# end def

# import logging;logging.basicConfig(level=logging.DEBUG); from database_migrations import do_update