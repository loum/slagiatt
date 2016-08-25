"""Tests for the :class:`slagiatt.route.Device`.
"""
import os
import json
import unittest

import slagiatt
import slagiatt.common
import slagiatt.tests


class TestDevice(unittest.TestCase):
    """Test file for the Zabbix Device Management API.

    """
    @classmethod
    def setUpClass(cls):
        cls.__client = slagiatt.APP.test_client()

    def setUp(self):
        slagiatt.common.BASE.metadata.create_all()

    def tearDown(self):
        slagiatt.common.BASE.metadata.drop_all()

    def load_sample_device_data(self):
        """Helper to load data into the test DB table.

        """
        source_file = os.path.join('slagiatt',
                                   'tests',
                                   'factory',
                                   'files',
                                   'device.json')

        table_name = 'slagiatt.tests.factory.Device'
        table_obj = slagiatt.tests.Table(table_name)
        table_obj.load(source_file)


    def test_device_insert(self):
        """Test a device insert (POST).
        """
        # Given a valid endpoint to add a new device configuration
        url = '/api/device'

        # and a payload
        payload = {
            'equip_inst_id': 211753,
            'physical_name': '2ABN-01-01-PSY',
            'physical_name_extn': '0001',
            'nw_ip_addr': '10.35.222.58',
            'equip_inst_id_1': '211753',
            'equip_status_id': 3
        }

        # when I submit a new device request
        response = self.__client.post(url,
                                      data=json.dumps(payload),
                                      content_type='application/json')

        # then I should receive a HTTP 201 "Accepted" response
        msg = 'device POST did not return 201'
        self.assertEqual(response.status_code, 201, msg)

    def test_device_insert_malformed_payload(self):
        """Test a device insert (POST): malformed payload.
        """
        # Given a valid endpoint to add a new device configuration
        url = '/api/device'

        # and a malformed payload
        payload = {
            'equip_inst_id': 211753,
            'physical_name': '2ABN-01-01-PSY',
            'physical_name_extn': '0001',
            'nw_ip_addr': '10.35.222.58',
            'equip_inst_id_1': '211753',
            'equip_status_id': 3,
            'banana': None,
        }

        # when I submit a new device request
        response = self.__client.post(url,
                                      data=json.dumps(payload),
                                      content_type='application/json')

        # then I should receive a HTTP 400 "Bad Request" response
        msg = 'device POST did not return 400'
        self.assertEqual(response.status_code, 400, msg)

    def test_device_query_device_not_found(self):
        """Test a device insert (GET): device not found.
        """
        # Given a valid endpoint to query device configuration
        url = '/api/device'

        # and query parameters
        data = {
            'q': json.dumps({'equip_inst_id': 21175})
        }

        # when I submit the query
        response = self.__client.get(url, query_string=data)

        # then I should receive a HTTP 200 "OK" response
        msg = 'device POST did not return 200'
        self.assertEqual(response.status_code, 200, msg)

        # and the response data should indicate no match
        received = json.loads(response.data.decode('utf-8'))
        expected = {
            'num_results': 0,
            'objects': [],
            'page': 1, 'total_pages': 0
        }
        msg = 'device POST did not return 200'
        self.assertDictEqual(received, expected, msg)

    def test_device_query_parameter_based_no_match(self):
        """Test a device insert (GET): parameter based no match.
        """
        # Given a valid endpoint to query device configuration
        url = '/api/device'

        # and query parameters
        data = {
            'q': json.dumps({'equip_inst_id': 21175})
        }

        # when I submit the query
        response = self.__client.get(url, query_string=data)

        # then I should receive a HTTP 200 "OK" response
        msg = 'device POST did not return 200'
        self.assertEqual(response.status_code, 200, msg)

        # and the response data should indicate no match
        received = json.loads(response.data.decode('utf-8'))
        expected = {
            'num_results': 0,
            'objects': [],
            'page': 1, 'total_pages': 0
        }
        msg = 'device POST response data error'
        self.assertDictEqual(received, expected, msg)

    def test_device_query_parameter_based_expecting_match(self):
        """Test a device insert (GET): parameter based expected match.
        """
        # Given a valid endpoint to query device configuration
        url = '/api/device'

        # and query parameters
        data = {
            'q': json.dumps({'equip_inst_id': 211753})
        }

        # when I submit the query
        self.load_sample_device_data()
        response = self.__client.get(url, query_string=data)

        # then I should receive a HTTP 200 "OK" response
        msg = 'device POST did not return 200'
        self.assertEqual(response.status_code, 200, msg)

        # and the response data should indicate no match
        received = json.loads(response.data.decode('utf-8'))
        expected = {
            'num_results': 1,
            'objects': [
                {
                    'equip_inst_id': 211753,
                    'equip_inst_id_1': 211753,
                    'equip_status_id': 3,
                    'nw_ip_addr': '10.35.222.58',
                    'physical_name': '2ABN-01-01-PSY',
                    'physical_name_extn': '0001'
                }
            ],
            'page': 1,
            'total_pages': 1
        }
        msg = 'device POST reponse data error'
        self.assertDictEqual(received, expected, msg)

    def test_device_delete(self):
        """Test a device delete (DELETE).
        """
        # Given a valid endpoint to query device configuration
        url = '/api/device/211753'

        # when I submit the delete request
        self.load_sample_device_data()
        response = self.__client.delete(url)

        # then I should receive a HTTP 204 "No Content" response
        msg = 'device POST did not return 204'
        self.assertEqual(response.status_code, 204, msg)

    def test_device_delete_no_match(self):
        """Test a device delete (DELETE): no match.
        """
        # Given a valid endpoint to query device configuration
        url = '/api/device/211753'

        # when I submit the delete request
        response = self.__client.delete(url)

        # then I should receive a HTTP 404 "No Content" response
        msg = 'device POST did not return 404'
        self.assertEqual(response.status_code, 404, msg)
