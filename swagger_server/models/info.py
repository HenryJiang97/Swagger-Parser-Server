from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Info(Model):

    def __init__(self, title: str=None, version: str=None, description: str=None):  # noqa: E501
        """Info - a model defined in Swagger

        :param title: The title of this Info.  # noqa: E501
        :type title: str
        :param version: The version of this Info.  # noqa: E501
        :type version: str
        :param description: The description of this Info.  # noqa: E501
        :type description: str
        """
        self.swagger_types = {
            'title': str,
            'version': str,
            'description': str
        }

        self.attribute_map = {
            'title': 'title',
            'version': 'version',
            'description': 'description'
        }

        self._title = title
        self._version = version
        self._description = description

    @classmethod
    def from_dict(cls, dikt) -> 'Info':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Info of this Info.  # noqa: E501
        :rtype: Info
        """
        return util.deserialize_model(dikt, cls)

    @property
    def title(self) -> str:
        """Gets the title of this Info.

        :return: The title of this Info.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title: str):
        """Sets the title of this Info.

        :param title: The title of this Info.
        :type title: str
        """
        if title is None:
            raise ValueError("Invalid value for `title`, must not be `None`")  # noqa: E501

        self._title = title

    @property
    def version(self) -> str:
        """Gets the version of this Info.

        :return: The version of this Info.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version: str):
        """Sets the version of this Info.

        :param version: The version of this Info.
        :type version: str
        """
        if version is None:
            raise ValueError("Invalid value for `version`, must not be `None`")  # noqa: E501

        self._version = version

    @property
    def description(self) -> str:
        """Gets the description of this Info.

        :return: The description of this Info.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description: str):
        """Sets the description of this Info.

        :param description: The description of this Info.
        :type description: str
        """

        self._description = description
