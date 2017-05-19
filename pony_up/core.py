from luckydonaldUtils.exceptions import assert_type_or_raise
from pony import orm


class Migrator(object):
    def __init__(self, old_db, new_db, bind_database_function, old_version, has_new_schema=False):
        assert_type_or_raise(old_db, (None, orm.Database))
        self.old_db = old_db

        assert_type_or_raise(new_db, (None, orm.Database))
        self.new_db = new_db

        assert_type_or_raise(old_version, int)
        self.old_version = old_version

        self.bind_database_function = bind_database_function

        assert_type_or_raise(has_new_schema, bool)
        self.has_new_schema = has_new_schema
    # end def

    def __str__(self):
        return "{s.__class__.__name__}(old_db={s.old_db}, new_db={s.new_db}, bind_database_function={s.bind_database_function}, " \
               "old_version={s.old_version}, has_new_schema={s.has_new_schema})".format(s=self)
# end class
