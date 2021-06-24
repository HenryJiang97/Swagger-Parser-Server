from flask import make_response, jsonify

from swagger_server.models.error import Error
from swagger_server.models.swagger_spec import SwaggerSpec
from swagger_server.models.parse_data import ParseData

from swagger_server.models.exceptions.parse_exception import ParseException
from swagger_server.models.exceptions.file_not_found_exception import FileNotFoundException
from swagger_server.models.exceptions.db_connection_exception import DBConnectionException

from swagger_server.db.db import Database
from swagger_server.service.parser import Parser


def parse_id_get(id):  # noqa: E501
    """Parse an API file

     # noqa: E501

    :param id: File unique id
    :type id: 

    :rtype: ParseData
    """
    try:
        # Database connection
        db = Database()
        connection = db.connect()
        if connection is None:
            raise DBConnectionException

        # Database manipulation
        spec = db.select_by_id(id)
        if spec is None:
            raise FileNotFoundException

        # Parse
        spec_dict = SwaggerSpec.to_dict(spec)
        parser = Parser(swagger_dict=spec_dict)
        parser.build_info()
        parser.get_paths_data()
        parse_data = ParseData(
            parser.info,
            parser.base_path,
            parser.paths
        )

        return make_response(jsonify(parse_data), 200)

    except FileNotFoundException:
        e = Error("File not found")
        return make_response(jsonify(e), 404)

    except ParseException as e:
        e = Error(f"Parse exception: {str(e)}")
        return make_response(jsonify(e), 400)

    except DBConnectionException:
        e = Error("Database connection error")
        return make_response(jsonify(e), 500)

    except Exception as e:
        return make_response(jsonify(e), 503)
