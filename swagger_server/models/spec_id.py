from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class SpecId(Model):

    def __init__(self, id):  # noqa: E501
        self.swagger_types = {
            'id': id
        }

        self.attribute_map = {
            'id': 'id'
        }

        self._id = id

    @classmethod
    def from_dict(cls, dikt) -> 'SpecId':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The SpecId of this SpecId.  # noqa: E501
        :rtype: SpecId
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> str:
        """Gets the id of this PeekData.

        :return: The id of this PeekData.
        :rtype: SpecId
        """
        return self._id

    @id.setter
    def id(self, id: str):
        """Sets the id of this SpecId.

        :param id: The id of this SpecId.
        :type id: string
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id