"""Class definition for test Table implementation.
"""
import importlib
import json
import sqlalchemy.exc
from logga import log


class Table(object):
    """
    .. attribute:: table

        :mod:`slagiatt.model` table class mapping

    """
    def __init__(self, table):
        self.__table = table

    @property
    def table(self):
        return self.to_instance()

    @table.setter
    def table(self, value):
        self.__table = value

    def to_instance(self):
        """Convert string representation of a :attr:`table` name to an
        actual class instance.

        """
        tmp_table = self.__table

        if isinstance(tmp_table, str):
            components = tmp_table.split('.')
            klass = components[-1]
            mod = importlib.import_module('.'.join(components[:-1]))

            if hasattr(mod, klass):
                tmp_table = getattr(mod, klass)
            else:
                log.error('Unable to convert "%s" to a class', tmp_table)
                tmp_table = None

        return tmp_table

    def load(self, file_path):
        """Load source JSON files into DB.

        JSON format should be a list of column named values.

        **Args:**
            *file_path*: path to JSON file that will be loaded into
            :attr:`table`

        """
        log.info('Transforming "%s" to DB', file_path)

        data = None
        try:
            with open(file_path) as _fh:
                try:
                    data = json.loads(_fh.read().rstrip())
                except json.decoder.JSONDecodeError as err:
                    log.error('"%s" JSON decode error: "%s"',
                              file_path, err)
                    data = []
        except (OSError, IOError) as err:
            log.error(err)

        inserted = 0
        rejected = 0
        for row in data or []:
            self.table(**row)

            try:
                self.table._meta.sqlalchemy_session.commit()
                inserted += 1
            except sqlalchemy.exc.SQLAlchemyError as err:
                log.error('Source DB insert error: "%s"', err)
                rejected += 1
                self.table._meta.sqlalchemy_session.rollback()

        log.info('Inserted|rejected %d|%d records into table "%s"',
                 inserted, rejected, self.table._meta.model.__tablename__)

        return (inserted, rejected)
