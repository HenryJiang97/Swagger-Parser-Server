import connexion
import six

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.peek_data import PeekData  # noqa: E501
from swagger_server.models.spec_id import SpecId  # noqa: E501
from swagger_server.models.success import Success  # noqa: E501
from swagger_server.models.swagger_spec import SwaggerSpec  # noqa: E501
from swagger_server.models.upload import Upload  # noqa: E501
from swagger_server import util

from ..db.db import Database


def swaggerspec_post(body):  # noqa: E501
    """Upload .yaml file, validate and save JSON format to database.

     # noqa: E501

    :param body: Upload file data
    :type body: dict | bytes

    :rtype: SpecId
    """
    try:
        if connexion.request.is_json:
            body = Upload.from_dict(connexion.request.get_json())  # noqa: E501

        db = Database()
        db.connect()

        return db.insert(body.name, body.file)
    except ConnectionError as e:
        return Error(e)


def swaggerspec_delete():  # noqa: E501
    """Delete all files existing in database.

     # noqa: E501


    :rtype: Success
    """
    try:
        db = Database()
        db.connect()
        return db.clear()
    except ConnectionError as e:
        return Error(e)


def swaggerspec_get():  # noqa: E501
    """List all files existing in database.

     # noqa: E501


    :rtype: List[PeekData]
    """
    try:
        db = Database()
        db.connect()
        return db.select_all()
    except ConnectionError as e:
        return Error(e)


def swaggerspec_id_delete(id):  # noqa: E501
    """Delete spec file by id from database.

     # noqa: E501

    :param id: File unique id
    :type id: 

    :rtype: Success
    """
    return 'do some magic!'


def swaggerspec_id_get(id):  # noqa: E501
    """Get spec file by id from database.

     # noqa: E501

    :param id: File unique id
    :type id: 

    :rtype: SwaggerSpec
    """
    return 'do some magic!'


def swaggerspec_id_put(id):  # noqa: E501
    """Update spec file by id from database.

     # noqa: E501

    :param id: File unique id
    :type id: 

    :rtype: Success
    """
    return 'do some magic!'
