from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Error(Model):
    def __init__(self, error_message: str=None):  # noqa: E501
        """Error - a model defined in Swagger

        :param error_message: The error_message of this Error.  # noqa: E501
        :type error_message: str
        """
        self.swagger_types = {
            'error_message': str
        }

        self.attribute_map = {
            'error_message': 'ErrorMessage'
        }

        self._error_message = error_message

    @classmethod
    def from_dict(cls, dikt) -> 'Error':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Error of this Error.  # noqa: E501
        :rtype: Error
        """
        return util.deserialize_model(dikt, cls)

    @property
    def error_message(self) -> str:
        """Gets the error_message of this Error.

        :return: The error_message of this Error.
        :rtype: str
        """
        return self._error_message

    @error_message.setter
    def error_message(self, error_message: str):
        """Sets the error_message of this Error.

        :param error_message: The error_message of this Error.
        :type error_message: str
        """
        if error_message is None:
            raise ValueError("Invalid value for `error_message`, must not be `None`")  # noqa: E501

        self._error_message = error_message
