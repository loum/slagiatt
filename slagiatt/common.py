"""Common SLAGIATT attributes file
"""
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import logging
logging.getLogger('factory').setLevel(logging.WARN)

import slagiatt.db


class Base(object):
    """The :class:`Base` defines SQLAlchemy **Declarative** system that
    forms the basis for describing the database tables we'll be dealing
    with.  Each Python class will be mapped to an actual DB tables.

    The SQLAlchemy Declarative system which allows us to create classes
    that include directives to describe the actual database table they
    will be mapped to.

    Classes mapped using the Declarative system are defined in terms of
    this base class which maintains a catalog of classes and tables
    relative to that base.  The aim here is to limit to just one
    instance of this base in a commonly imported module.

    """
    @sqlalchemy.ext.declarative.declared_attr
    def __tablename__(cls):
        """Fall back to the class name (in lowercase)
        if a class ``__tablename__`` is not provided.

        """
        table_name = None

        if hasattr(cls, '__name__'):
            table_name = cls.__name__.lower()

        return table_name


BASE = sqlalchemy.ext.declarative.declarative_base(cls=Base)

SESSION = sqlalchemy.orm.scoped_session(sqlalchemy.orm.sessionmaker())

# The DB context.
DB = slagiatt.db.Db()
