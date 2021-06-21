import connexion
import six

from flask import make_response

from swagger_server.models.success import Success  # noqa: E501
from swagger_server.models.error import Error
from swagger_server.models.swagger_spec import SwaggerSpec  # noqa: E501

from swagger_server.models.exceptions.invalid_spec_exception import InvalidSpecException

from openapi_spec_validator import validate_v2_spec
from openapi_spec_validator import validate_v3_spec


def validate_post(body):  # noqa: E501
    """Validate the specs of an API file

     # noqa: E501

    :param body: API file data
    :type body: dict | bytes

    :rtype: Success
    """
    if connexion.request.is_json:
        body = SwaggerSpec.from_dict(connexion.request.get_json())  # noqa: E501

    try:
        spec_dict = SwaggerSpec.to_dict(body)
        api_version = body.swagger if body.swagger is not None else body.openapi

        if '2.0' <= api_version < '3.0':
            # Swagger 2.0
            validate_v2_spec(spec_dict)
        else:
            # Openapi 3.0
            validate_v3_spec(spec_dict)

        response = Success("Valid spec")
        return make_response(Success.to_dict(response), 200)

    except InvalidSpecException:
        e = Error("Invalid spec")
        return make_response(Error.to_dict(e), 400)

    except Exception as e:
        e = Error(e)
        return make_response(Error.to_dict(e), 503)

