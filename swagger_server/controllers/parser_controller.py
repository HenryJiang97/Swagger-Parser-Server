import connexion
import six

from swagger_server.models.swagger_spec import SwaggerSpec
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.parse_data import ParseData  # noqa: E501

from swagger_server.db.db import Database
from swagger_server.service.parser import Parser

from swagger_server import util


def parse_id_get(id):  # noqa: E501
    """Parse an API file

     # noqa: E501

    :param id: File unique id
    :type id: 

    :rtype: ParseData
    """
    try:
        db = Database()
        db.connect()
        spec = db.select_by_id(id)
        spec_dict = SwaggerSpec.to_dict(spec)

        parser = Parser(swagger_dict=spec_dict)

        # Info
        parser.build_info()

        # Path
        parser.get_paths_data()

        parse_data = ParseData(
            parser.info,
            parser.base_path,
            parser.paths
        )

        return parse_data

    except Exception as e:
        return Error(e)

    return 'do some magic!'
