# -*- coding: utf-8 -*-
import importlib
import os

from luckydonaldUtils.logger import logging
from luckydonaldUtils.exceptions import assert_or_raise as assert_type_or_raise


__author__ = 'luckydonald'
logger = logging.getLogger(__name__)
from pony import orm

from datetime import datetime
from uuid import UUID, uuid4
from luckydonaldUtils.logger import logging

migrations = {}  # { old_version: module }


def enumerate_migrations(import_path):
    """Map the names of modules to the location of their file.
    Return a dict mapping the names of modules to the location of their
    file. If two modules have the same name, the last one to be found will be
    returned and the rest will be ignored. Modules are found in the
    ./migrations/ folder, relative to (also next to) this python file.
    Taken from https://github.com/luckydonald/bonbot/blob/1d8c262c6ca99000346c41fbb4b88ab00c7aad5a/Bonbot/Plugin/__init__.py#L286
    Changes under the MIT, (c) luckydonald 2014-2017.
    Taken from https://github.com/embolalia/willie/blob/690eeaf30e99f9e58b0c648c9881fe30d4b14ade/willie/config.py#L339;
    (Licensed under the Eiffel Forum License 2. Original copyright:
    "Copyright 2012, Edward Powell, embolalia.net" and "Copyright © 2012, Elad Alfassa <elad@fedoraproject.org>")
    """
    modules = {}

    # First, add modules from the regular modules directory
    this_dir = os.path.dirname(os.path.abspath(__file__))
    modules_dir = os.path.join(this_dir, import_path)
    for filename in os.listdir(modules_dir):
        file_path = os.path.abspath(os.path.join(modules_dir, filename))
        if filename.endswith('.py') and not filename.startswith('_'):
            modules[filename[:-3]] = file_path
            logger.debug("found python file:    {file}".format(file=file_path))
        elif os.path.isdir(file_path) and os.path.exists(os.path.join(file_path, "__init__.py")):
            modules[filename] = file_path
            logger.debug("found python package: {file}".format(file=file_path))
        # end if
    return modules
# end def


def get_current_version(db):
    """
    This loads the current version from the database.
    If there is no version stored, a version 0 will get stored (and returned) 
    
    :param db: the database
    :return: the entry from the version database
    """
    Version = db.entities["Version"]
    assert_type_or_raise(Version, orm.core.EntityMeta, orm.core.Entity)

    db_versions = orm.select(v for v in Version).order_by(orm.desc(Version.version)).limit(1)
    if len(db_versions) != 0:
        db_version = db_versions[0]
    else:
        db_version = store_new_version(db, 0, meta={"message": "initial creation"})
    # end def
    return db_version
# end def


def do_version(version_module, old_db=None):
    """
    Creates a new db, registers vNEW model, and runs migrate.do_update(old_db, vNEW_db)
     
    :param version_module: 
    :param old_db: 
    :return: 
    """
    print("do_update: do_version")
    db = orm.Database()
    version_module.model.register_database(db)
    bind_database(db)
    if hasattr(version_module, "migrate"):
        return db, version_module.migrate.do_update(db, old_db)
    # end def
    return db, None
# end def


def bind_database(db):
    """
    Creates the bind command and connects a postgres database.
    
    :param db: 
    :return: 
    """
    from secrets import POSTGRES_HOST, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB
    db.bind("postgres", host=POSTGRES_HOST, user=POSTGRES_USER, password=POSTGRES_PASSWORD, database=POSTGRES_DB)
    db.generate_mapping(create_tables=True)
    logger.debug(
        "Generated Schema: \n===SQL===\n" + db.schema.generate_create_script() + "\n===END===")
    return db
# end def

@orm.db_session
def store_new_version(db, version_no, meta=None):
    """
    This writes a database version to the db.
    :param db: database 
    :param version_no: new version int 
    :param meta: any json
    :return: the provided version.
    """
    logger.debug("storing new version {v!r} with metadata {meta!r}.".format(v=version_no, meta=meta))
    Version = db.entities["Version"]
    assert_type_or_raise(Version, orm.core.EntityMeta, orm.core.Entity)
    new_version_entry = Version(version=version_no, meta=meta)
    return new_version_entry
# end def


def do_all_migrations(import_path="migrations", relative_import="database_migrations.migrations"):
    from . import version_db

    db = orm.Database()
    version_db.register_database(db)
    bind_database(db)
    current_version_db = get_current_version(db)
    db_version = current_version_db.version
    del db

    file_names_found = enumerate_migrations(import_path)
    logger.debug("migration files: {!r}".format(file_names_found))
    for name, file_name in dict.items(file_names_found):
        logger.debug("name {!r}, file_name {!r}".format(name, file_name))
        if not name.startswith("v"):
            logger.debug("skipping module, format wrong.\nExpected 'v{{number}}', got {module_name!r}".format(module_name=name))
            continue
        # end def
        try:
            version = int(name[1:])
        except:
            logger.debug("skipping module, version int malformatted.\nExpected 'v{{number}}', got {module_name!r}".format(module_name=name))
            continue
        # end try
        if version < db_version:
            logger.debug("skipping module, version {load!r} smaller than current {db!r}.".format(load=version, db=db_version))
            continue
        # end def
        module = importlib.import_module(relative_import + "." + name)
        logger.debug("version {!r}: name {!r}, file_name {!r}, module {!r}".format(version, name, file_name, module.__name__))

        migrations[version] = module
    # end for

    db = None
    # iterate though the versions:
    for v, module in sorted(migrations.items(), key=lambda x: x[0]):
        logger.debug("preparing update from version {v!r}".format(v=v))
        if hasattr(module, "migrate"):
            logger.debug("applying migrations from version {v!r}".format(v=v))
            db, version_meta = do_version(module, old_db=db)
            new_version, meta = version_meta
            store_new_version(db, new_version, meta)
            logger.success("Upgraded to version {v!r} {meta!r}".format(v=v, meta=repr(meta["message"]) if "message" in meta else "").strip())
        else:
            db = orm.Database()
            module.model.register_database(db)
            bind_database(db)
        # end if
    # end for
    return db
# end def

db = do_all_migrations()
