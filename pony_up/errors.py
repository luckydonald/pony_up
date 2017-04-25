from pony.orm.core import OrmError


class VersionTableAlreadyExists(OrmError):
    """
    Is raised when the `Version` table (see `pony_up.version_db.register_database(...)`
    already exists in to a database schema (type `pony.orm.core.Database`).
    
    Probably you included a table called `Version` in your own migration ,too?
    Don't do that :D
    """
    pass
# end class
