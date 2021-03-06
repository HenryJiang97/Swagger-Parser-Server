from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Paths(Model):

    def __init__(self):  # noqa: E501
        """Paths - a model defined in Swagger

        :param paths: The paths of this Paths.  # noqa: E501
        :type paths: paths
        """
        self.swagger_types = {
        }

        self.attribute_map = {
        }

    @classmethod
    def from_dict(cls, dikt) -> 'Paths':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Paths of this Paths.  # noqa: E501
        :rtype: Paths
        """
        return util.deserialize_model(dikt, cls)
