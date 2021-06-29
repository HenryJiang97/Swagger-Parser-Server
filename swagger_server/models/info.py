from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Info(Model):

    def __init__(self, title: str=None, version: str=None, description: str=None, base_path: str=None, host: str=None, servers: List[object]=None):  # noqa: E501
        """Info - a model defined in Swagger

        :param title: The title of this Info.  # noqa: E501
        :type title: str
        :param version: The version of this Info.  # noqa: E501
        :type version: str
        :param description: The description of this Info.  # noqa: E501
        :type description: str
        :param host: The host of this Info.  # noqa: E501
        :type host: str
        :param base_path: The base_path of this Info.  # noqa: E501
        :type base_path: str
        :param servers: The servers of this Info.  # noqa: E501
        :type servers: str
        """
        self.swagger_types = {
            'title': str,
            'version': str,
            'description': str,
            'host': str,
            'base_path': str,
            'servers': List[object]
        }

        self.attribute_map = {
            'title': 'title',
            'version': 'version',
            'description': 'description',
            'host': 'host',
            'base_path': 'basePath',
            'servers': 'servers'
        }

        self._title = title
        self._version = version
        self._description = description
        self._host = host
        self._base_path = base_path
        self._servers = servers

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

    @property
    def host(self) -> str:
        """Gets the host of this Info.

        :return: The host of this Info.
        :rtype: str
        """
        return self._host

    @host.setter
    def host(self, host: str):
        """Sets the host of this Info.

        :param host: The host of this Info.
        :type host: str
        """

        self._host = host

    @property
    def base_path(self) -> str:
        """Gets the base_path of this Info.

        :return: The base_path of this Info.
        :rtype: str
        """
        return self._base_path

    @base_path.setter
    def base_path(self, base_path: str):
        """Sets the base_path of this Info.

        :param base_path: The description of this Info.
        :type base_path: str
        """

        self._base_path = base_path

    @property
    def servers(self) -> List[object]:
        """Gets the servers of this Info.

        :return: The servers of this Info.
        :rtype: List[object]
        """
        return self._servers

    @servers.setter
    def servers(self, servers: List[object]):
        """Sets the servers of this Info.

        :param servers: The description of this Info.
        :type servers: str
        """

        self._servers = servers
