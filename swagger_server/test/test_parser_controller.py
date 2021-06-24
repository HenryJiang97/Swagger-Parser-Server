# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.test import BaseTestCase


class TestParserController(BaseTestCase):
    """ParserController integration test stubs"""

    def test_parse_id_get(self):
        """Test case for parse_id_get

        Parse an API file
        """
        response = self.client.open(
            '//parse/{id}'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
