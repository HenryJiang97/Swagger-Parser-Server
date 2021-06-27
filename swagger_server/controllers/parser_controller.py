from flask import make_response, jsonify

from swagger_server.models.error import Error
from swagger_server.models.swagger_spec import SwaggerSpec
from swagger_server.models.info import Info
from swagger_server.models.paths import Paths

from swagger_server.models.exceptions.parse_exception import ParseException
from swagger_server.models.exceptions.file_not_found_exception import FileNotFoundException
from swagger_server.models.exceptions.db_connection_exception import DBConnectionException

from swagger_server.db.db import Database
from swagger_server.service.parser import Parser


def parse_info_id_get(id):  # noqa: E501
    """Parse spec info

    :param id: File unique id
    :type id:

    :rtype: Info
    """
    try:
        # Database connection
        db = Database()
        connection = db.connect()
        if connection is None:
            raise DBConnectionException

        # Database manipulation
        spec = db.select_spec_by_id(id)
        if spec is None:
            raise FileNotFoundException

        # Parse
        spec_dict = SwaggerSpec.to_dict(spec)
        parser = Parser(swagger_dict=spec_dict)
        parser.build_info()
        info = Info.from_dict(parser.info)

        return make_response(jsonify(info), 200)

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
        return make_response(str(e), 503)


def parse_paths_id_get(id):
    """Parse spec paths

    :param id: File unique id
    :type id:

    :rtype: Paths
    """
    try:
        # Database connection
        db = Database()
        connection = db.connect()
        if connection is None:
            raise DBConnectionException

        # Database manipulation
        spec = db.select_spec_by_id(id)
        if spec is None:
            raise FileNotFoundException

        # Parse
        spec_dict = SwaggerSpec.to_dict(spec)
        parser = Parser(swagger_dict=spec_dict)
        parser.get_paths_data()
        paths = Paths.from_dict(parser.paths)

        return make_response(jsonify(paths), 200)

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
        return make_response(str(e), 503)
