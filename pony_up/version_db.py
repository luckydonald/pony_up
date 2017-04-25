"""
This module contains the definition of the `Version` table (`pony.orm.Entity`)
to be used to store informations about the versions.

Call `register_database(db)` to appy this mapping to a database (`pony.orm.Database`).
"""

from datetime import datetime
from pony import orm


def register_database(db):
    """
    Applies the `Version` table to the given database.
    
    :param db: the database
    :type  db: pony.orm.code.Database
    :return: 
    """
    class Version(db.Entity):
        version = orm.PrimaryKey(int, auto=False)
        upgraded = orm.Required(datetime, sql_default='NOW()')
        meta = orm.Optional(orm.Json, lazy=True)
    # end class
# end def