import unittest

import slagiatt


class TestHealth(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.__client = slagiatt.APP.test_client()

    def test_health(self):
        """Test the health URL.
        """
        response = self.__client.get('/health')
        msg = 'Health check response'
        code_msg = '{} code error'.format(msg)
        self.assertEqual(response.status_code, 200, msg)
        data_msg = '{} data error'.format(msg)
        self.assertEqual(response.data, b'"Hey, I\'m OK"\n', msg)
