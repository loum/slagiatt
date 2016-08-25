"""SQLAlchemy DB connection abstraction layer.

"""
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative
from logga import log

import slagiatt.common


class Db(object):
    """Abstracts connection to the database.

    .. attribute:: dry

        Boolean value which if set, invoke mocks (does not hit
        production databases).

    .. attribute:: engine

        Handle to the target DB.

    """

    def __init__(self, dry=False):
        self.__dry = dry
        self.__engine = None
        self.__conn = None

    @property
    def dry(self):
        """:attr:`dry` getter.
        """
        return self.__dry

    @dry.setter
    def dry(self, value):
        """:attr:`dry` setter.
        """
        self.__dry = value

    @property
    def engine(self):
        """:attr:`engine` getter.
        """
        return self.__engine

    @engine.setter
    def engine(self, value):
        """:attr:`engine` setter.
        """
        self.__engine = value

    @property
    def conn(self):
        """:attr:`conn` getter.
        """
        return self.__conn

    @conn.setter
    def conn(self, value):
        """:attr:`conn` setter.
        """
        self.__conn = value

    def init(self, target=None):
        """Create the DB connection.

        **Kwargs:**
            *target*: additional value that can be passed to the
            underlying database dialect

        """
        log.info('Creating DB connection against target "%s"', target)
        args = [target]
        kwargs = {'echo': False}
        self.engine = sqlalchemy.create_engine(*args, **kwargs)

        slagiatt.common.SESSION.configure(bind=self.engine)

    def close(self):
        """Clean up the DB connection.

        """
        log.info('Closing DB connection')
        slagiatt.commom.SESSION.remove()
        if self.engine is not None:
            self.engine.dispose()
