from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Success(Model):

    def __init__(self, success_message: str=None):  # noqa: E501
        """Success - a model defined in Swagger

        :param success_message: The success_message of this Success.  # noqa: E501
        :type success_message: str
        """
        self.swagger_types = {
            'success_message': str
        }

        self.attribute_map = {
            'success_message': 'SuccessMessage'
        }

        self._success_message = success_message

    @classmethod
    def from_dict(cls, dikt) -> 'Success':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Success of this Success.  # noqa: E501
        :rtype: Success
        """
        return util.deserialize_model(dikt, cls)

    @property
    def success_message(self) -> str:
        """Gets the success_message of this Success.

        :return: The success_message of this Success.
        :rtype: str
        """
        return self._success_message

    @success_message.setter
    def success_message(self, success_message: str):
        """Sets the success_message of this Success.

        :param success_message: The success_message of this Success.
        :type success_message: str
        """
        if success_message is None:
            raise ValueError("Invalid value for `success_message`, must not be `None`")  # noqa: E501

        self._success_message = success_message
