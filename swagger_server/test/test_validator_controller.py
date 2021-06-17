# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.success import Success  # noqa: E501
from swagger_server.models.swagger_spec import SwaggerSpec  # noqa: E501
from swagger_server.test import BaseTestCase


class TestValidatorController(BaseTestCase):
    """ValidatorController integration test stubs"""

    def test_validate_post(self):
        """Test case for validate_post

        Validate the specs of an API file
        """
        body = SwaggerSpec()
        response = self.client.open(
            '//validate',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
