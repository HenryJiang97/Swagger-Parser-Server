# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.peek_data import PeekData  # noqa: E501
from swagger_server.models.spec_id import SpecId  # noqa: E501
from swagger_server.models.success import Success  # noqa: E501
from swagger_server.models.swagger_spec import SwaggerSpec  # noqa: E501
from swagger_server.models.upload import Upload  # noqa: E501
from swagger_server.test import BaseTestCase


class TestSpecController(BaseTestCase):
    """SpecController integration test stubs"""

    def test_swaggerspec_delete(self):
        """Test case for swaggerspec_delete

        Delete all files existing in database.
        """
        response = self.client.open(
            '//swaggerspec',
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_swaggerspec_get(self):
        """Test case for swaggerspec_get

        List all files existing in database.
        """
        response = self.client.open(
            '//swaggerspec',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_swaggerspec_id_delete(self):
        """Test case for swaggerspec_id_delete

        Delete spec file by id from database.
        """
        response = self.client.open(
            '//swaggerspec/{id}'.format(id='id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_swaggerspec_id_get(self):
        """Test case for swaggerspec_id_get

        Get spec file by id from database.
        """
        response = self.client.open(
            '//swaggerspec/{id}'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_swaggerspec_id_put(self):
        """Test case for swaggerspec_id_put

        Update spec file by id from database.
        """
        response = self.client.open(
            '//swaggerspec/{id}'.format(id='id_example'),
            method='PUT')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_swaggerspec_post(self):
        """Test case for swaggerspec_post

        Upload .yaml file, validate and save JSON format to database.
        """
        body = Upload()
        response = self.client.open(
            '//swaggerspec',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
