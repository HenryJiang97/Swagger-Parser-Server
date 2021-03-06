from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util

from ..models.swagger_spec import SwaggerSpec


class Upload(Model):

    def __init__(self, name: str=None, file: bytearray=None):  # noqa: E501
        """Upload - a model defined in Swagger

        :param name: The name of this Upload.  # noqa: E501
        :type name: str
        :param file: The file of this Upload.  # noqa: E501
        :type file: SwaggerSpec
        """
        self.swagger_types = {
            'name': str,
            'file': SwaggerSpec
        }

        self.attribute_map = {
            'name': 'name',
            'file': 'file'
        }

        self._name = name
        self._file = file

    @classmethod
    def from_dict(cls, dikt) -> 'Upload':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Upload of this Upload.  # noqa: E501
        :rtype: Upload
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self) -> str:
        """Gets the name of this Upload.

        :return: The name of this Upload.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this Upload.

        :param name: The name of this Upload.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def file(self) -> bytearray:
        """Gets the file of this Upload.

        :return: The file of this Upload.
        :rtype: SwaggerSpec
        """
        return self._file

    @file.setter
    def file(self, file: bytearray):
        """Sets the file of this Upload.

        :param file: The file of this Upload.
        :type file: SwaggerSpec
        """
        if file is None:
            raise ValueError("Invalid value for `file`, must not be `None`")  # noqa: E501

        self._file = file
