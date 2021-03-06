from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util

from ..models.spec_id import SpecId


class PeekData(Model):

    def __init__(self, id: SpecId=None, name: str=None, version: str=None):  # noqa: E501
        """PeekData - a model defined in Swagger

        :param id: The id of this PeekData.  # noqa: E501
        :type id: SpecId
        :param name: The name of this PeekData.  # noqa: E501
        :type name: str
        :param version: The version of this PeekData.  # noqa: E501
        :type version: str
        """
        self.swagger_types = {
            'id': SpecId,
            'name': str,
            'version': str
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'version': 'version'
        }

        self._id = id
        self._name = name
        self._version = version

    @classmethod
    def from_dict(cls, dikt) -> 'PeekData':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The PeekData of this PeekData.  # noqa: E501
        :rtype: PeekData
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> SpecId:
        """Gets the id of this PeekData.

        :return: The id of this PeekData.
        :rtype: SpecId
        """
        return self._id

    @id.setter
    def id(self, id: SpecId):
        """Sets the id of this PeekData.

        :param id: The id of this PeekData.
        :type id: SpecId
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def name(self) -> str:
        """Gets the name of this PeekData.

        :return: The name of this PeekData.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this PeekData.

        :param name: The name of this PeekData.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def version(self) -> str:
        """Gets the version of this PeekData.

        :return: The version of this PeekData.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version: str):
        """Sets the version of this PeekData.

        :param version: The version of this PeekData.
        :type version: str
        """
        if version is None:
            raise ValueError("Invalid value for `version`, must not be `None`")  # noqa: E501

        self._version = version
