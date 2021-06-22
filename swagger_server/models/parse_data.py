# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.path import Path
from swagger_server import util


class ParseData(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, info: object=None, base_path: str=None, paths: List[Path]=None):  # noqa: E501
        """ParseData - a model defined in Swagger

        :param info: The info of this ParseData.  # noqa: E501
        :type info: object
        :param base_path: The base_path of this ParseData.  # noqa: E501
        :type base_path: str
        :param paths: The paths of this ParseData.  # noqa: E501
        :type paths: List[Path]
        """
        self.swagger_types = {
            'info': object,
            'base_path': str,
            'paths': List[Path]
        }

        self.attribute_map = {
            'info': 'info',
            'base_path': 'basePath',
            'paths': 'paths'
        }

        self._info = info
        self._base_path = base_path
        self._paths = paths

    @classmethod
    def from_dict(cls, dikt) -> 'ParseData':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ParseData of this ParseData.  # noqa: E501
        :rtype: ParseData
        """
        return util.deserialize_model(dikt, cls)

    @property
    def info(self) -> object:
        """Gets the info of this ParseData.


        :return: The info of this ParseData.
        :rtype: object
        """
        return self._info

    @info.setter
    def info(self, info: object):
        """Sets the info of this ParseData.


        :param info: The info of this ParseData.
        :type info: object
        """

        self._info = info

    @property
    def base_path(self) -> str:
        """Gets the base_path of this ParseData.


        :return: The base_path of this ParseData.
        :rtype: str
        """
        return self._base_path

    @base_path.setter
    def base_path(self, base_path: str):
        """Sets the base_path of this ParseData.


        :param base_path: The base_path of this ParseData.
        :type base_path: str
        """
        if base_path is None:
            raise ValueError("Invalid value for `base_path`, must not be `None`")  # noqa: E501

        self._base_path = base_path

    @property
    def paths(self) -> List[Path]:
        """Gets the paths of this ParseData.


        :return: The paths of this ParseData.
        :rtype: List[Path]
        """
        return self._paths

    @paths.setter
    def paths(self, paths: List[Path]):
        """Sets the paths of this ParseData.


        :param paths: The paths of this ParseData.
        :type paths: List[Path]
        """
        if paths is None:
            raise ValueError("Invalid value for `paths`, must not be `None`")  # noqa: E501

        self._paths = paths
