"""Test for the :class:`slagiatt.tests.Table` helper.
"""
import os
import tempfile
import json
import unittest


import slagiatt.tests


class TestTable(unittest.TestCase):
    """Test for the :class:`slagiatt.tests.Table` helper.

    """
    def test_initialisation(self):
        """Test initialisation of a slagiatt.tests.Table instance.
        """
        # Given an API model table name
        table_name = 'slagiatt.model.Device'

        # when I initialise a slagiatt.tests.Table object
        table_obj = slagiatt.tests.Table(table_name)

        # then I should receive a slagiatt.tests.Table instance
        msg = 'Object is not a slagiatt.tests.Table instance'
        self.assertIsInstance(table_obj, slagiatt.tests.Table, msg)

    def test_to_instance(self):
        """Test translation of string table name to instance
        """
        # Given an API model table name
        table_name = 'slagiatt.model.Device'

        # when I translate the table to an instance
        table_obj = slagiatt.tests.Table(table_name)
        received = table_obj.to_instance()

        # then I should receive a slagiatt.model.Device instance
        msg = 'Object is not a slagiatt.model.Device instance'
        self.assertEqual(received, slagiatt.model.Device, msg)

    def test_load(self):
        """Load sample data into local table.
        """
        # Given an API model table name
        table_name = 'slagiatt.tests.factory.Device'

        # and a source JSON file
        source_file = os.path.join('slagiatt',
                                   'tests',
                                   'factory',
                                   'files',
                                   'device.json')

        # when I load into a local test table
        slagiatt.common.BASE.metadata.create_all()
        table_obj = slagiatt.tests.Table(table_name)
        received = table_obj.load(source_file)

        # then I should receive a count of 1 record inserted
        expected = (1, 0)
        msg = 'Sample insert count error'
        self.assertTupleEqual(received, expected, msg)

        # Clean up.
        slagiatt.common.BASE.metadata.drop_all()

    def test_load_missing_source_file(self):
        """Load sample data into local table: missing source file.
        """
        # Given an API model table name
        table_name = 'slagiatt.tests.factory.Device'

        # and an undefined source JSON file
        source_file = os.path.join('slagiatt',
                                   'tests',
                                   'factory',
                                   'files',
                                   'banana.json')

        # when I load into a local test table
        table_obj = slagiatt.tests.Table(table_name)
        received = table_obj.load(source_file)

        # then I should receive a count of 1 record inserted
        expected = (0, 0)
        msg = 'Sample insert count error'
        self.assertTupleEqual(received, expected, msg)

    def test_load_empty_source_file(self):
        """Load sample data into local table: empty source file.
        """
        # Given an API model table name
        table_name = 'slagiatt.tests.factory.Device'

        # and an undefined source JSON file
        source_file_obj = tempfile.NamedTemporaryFile()
        source_file = source_file_obj.name

        # when I load into a local test table
        table_obj = slagiatt.tests.Table(table_name)
        received = table_obj.load(source_file)

        # then I should receive a count of 1 record inserted
        expected = (0, 0)
        msg = 'Sample insert count error'
        self.assertTupleEqual(received, expected, msg)

    def test_load_empty_json_list(self):
        """Load sample data into local table: empty source JSON list.
        """
        # Given an API model table name
        table_name = 'slagiatt.tests.factory.Device'

        # and an undefined source JSON file
        source_file_obj = tempfile.NamedTemporaryFile('w')
        source_file_obj.write(json.dumps([]))
        source_file_obj.flush()
        source_file = source_file_obj.name

        # when I load into a local test table
        table_obj = slagiatt.tests.Table(table_name)
        received = table_obj.load(source_file)

        # then I should receive a count of 1 record inserted
        expected = (0, 0)
        msg = 'Sample insert count error'
        self.assertTupleEqual(received, expected, msg)
