import connexion
import six

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.success import Success  # noqa: E501
from swagger_server.models.swagger_spec import SwaggerSpec  # noqa: E501
from swagger_server import util


def validate_post(body):  # noqa: E501
    """Validate the specs of an API file

     # noqa: E501

    :param body: API file data
    :type body: dict | bytes

    :rtype: Success
    """
    if connexion.request.is_json:
        body = SwaggerSpec.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
