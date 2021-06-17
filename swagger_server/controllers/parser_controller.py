import connexion
import six

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.parse_data import ParseData  # noqa: E501
from swagger_server import util


def parse_id_get(id):  # noqa: E501
    """Parse an API file

     # noqa: E501

    :param id: File unique id
    :type id: 

    :rtype: ParseData
    """
    return 'do some magic!'
