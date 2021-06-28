import yaml
import json
import io
from flask import make_response, jsonify, send_file
from openapi_spec_validator import validate_v2_spec, validate_v3_spec

# Models
from swagger_server.models.error import Error
from swagger_server.models.spec_id import SpecId
from swagger_server.models.success import Success
from swagger_server.models.swagger_spec import SwaggerSpec

# Exceptions
from swagger_server.models.exceptions.file_not_found_exception import FileNotFoundException
from swagger_server.models.exceptions.db_connection_exception import DBConnectionException
from swagger_server.models.exceptions.duplicate_file_exception import DuplicateFileException
from swagger_server.models.exceptions.invalid_spec_exception import InvalidSpecException
from swagger_server.models.exceptions.invalid_content_type_exception import InvalidContentTypeException

# Database
from swagger_server.db.db import Database

# Accepted file types
_CONTENT_TYPES = set(['application/json', 'text/yaml'])


def swaggerspec_post(upfile=None):  # noqa: E501
    """Upload spec (.yaml or .json) file, validate and save raw file and JSON format spec to database.

    :param upfile: Upload file data
    :type upfile: formData

    :rtype: SpecId
    """
    try:
        # Get raw file
        filename = upfile.filename
        content_type = upfile.content_type
        if content_type not in _CONTENT_TYPES:
            raise InvalidSpecException("content type")

        # Get spec dict
        stream = upfile.stream
        raw = stream.read()
        spec_dict = None

        # Pre-processing
        if content_type == "application/json":
            spec_dict = json.loads(raw)
        if content_type == "text/yaml":
            spec_dict = yaml.safe_load(raw)

        # Validate spec
        try:
            api_version = spec_dict['swagger'] if "swagger" in spec_dict else spec_dict['openapi']

            if '2.0' <= api_version < '3.0':
                # Swagger 2.0
                validate_v2_spec(spec_dict)
            else:
                # Openapi 3.0
                validate_v3_spec(spec_dict)
        except Exception as e:
            raise InvalidSpecException(e)

        # Database connection
        db = Database()
        connection = db.connect()
        if connection is None:
            raise DBConnectionException

        # Database manipulation
        ret = db.insert(filename, SwaggerSpec.from_dict(spec_dict), content_type, raw)
        if ret is None:
            raise DuplicateFileException

        return make_response(jsonify(ret), 200)

    except InvalidSpecException as e:
        e = Error(f"Invalid spec: {str(e)}")
        return make_response(jsonify(e), 400)

    except DuplicateFileException:
        e = Error("File existed")
        return make_response(jsonify(e), 409)

    except DBConnectionException:
        e = Error("Database connection error")
        return make_response(jsonify(e), 500)

    except Exception as e:
        return make_response(str(e), 503)


def swaggerspec_delete():
    """Delete all specs existing in database.

    :rtype: Success
    """
    try:
        # Database connection
        db = Database()
        connection = db.connect()
        if connection is None:
            raise DBConnectionException

        # Database manipulation
        db.clear()

        response = Success("Table cleared")
        return make_response(jsonify(response), 200)

    except DBConnectionException:
        e = Error("Database connection error")
        return make_response(jsonify(e), 500)

    except Exception as e:
        return make_response(str(e), 503)


def swaggerspec_get():
    """List all specs existing in database.

    :rtype: List[PeekData]
    """
    try:
        # Database connection
        db = Database()
        connection = db.connect()
        if connection is None:
            raise DBConnectionException

        # Database manipulation
        ret = db.select_all()

        return make_response(jsonify(ret), 200)

    except DBConnectionException:
        e = Error("Database connection error")
        return make_response(jsonify(e), 500)

    except Exception as e:
        return make_response(str(e), 503)


def swaggerspec_id_get(id):
    """Get raw file by id from database.

    :param id: File unique id
    :type id: str

    :rtype: binary
    """
    try:
        # Database connection
        db = Database()
        connection = db.connect()
        if connection is None:
            raise DBConnectionException

        # Database manipulation
        ret = db.select_by_id(id)
        if ret is None:
            raise FileNotFoundException

        # Raw file details
        filename = ret[0]
        content_type = ret[1]
        raw = ret[2]

        return send_file(
            io.BytesIO(raw),
            mimetype=content_type,
            attachment_filename=filename
        )

    except FileNotFoundException:
        e = Error("File not found")
        return make_response(jsonify(e), 404)

    except DBConnectionException:
        e = Error("Database connection error")
        return make_response(jsonify(e), 500)

    except Exception as e:
        return make_response(str(e), 503)


def swaggerspec_id_delete(id):
    """Delete spec file by id from database.

    :param id: File unique id
    :type id: str

    :rtype: Success
    """
    try:
        # Database connection
        db = Database()
        connection = db.connect()
        if connection is None:
            raise DBConnectionException

        # Database manipulation
        ret = db.delete_by_id(id)
        if ret is None:
            raise FileNotFoundException

        response = Success("Deleted successfully")
        return make_response(jsonify(response), 200)

    except FileNotFoundException:
        e = Error("File not found")
        return make_response(jsonify(e), 404)

    except DBConnectionException:
        e = Error("Database connection error")
        return make_response(jsonify(e), 500)

    except Exception as e:
        return make_response(str(e), 503)


def swaggerspec_id_put(id, upfile=None):
    """Update spec file by id from database.

    :param id: File unique id
    :type id:
    :param upfile: Updated spec
    :type upfile: formData

    :rtype: Success
    """
    try:
        # Get raw file
        filename = upfile.filename
        content_type = upfile.content_type
        if content_type not in _CONTENT_TYPES:
            raise InvalidSpecException("content type")

        # Get spec dict
        stream = upfile.stream
        raw = stream.read()
        spec_dict = None

        # Pre-processing
        if content_type == "application/json":
            spec_dict = json.loads(raw)
        if content_type == "text/yaml":
            spec_dict = yaml.safe_load(raw)

        # Validate spec
        try:
            api_version = spec_dict['swagger'] if "swagger" in spec_dict else spec_dict['openapi']

            if '2.0' <= api_version < '3.0':
                # Swagger 2.0
                validate_v2_spec(spec_dict)
            else:
                # Openapi 3.0
                validate_v3_spec(spec_dict)
        except Exception as e:
            raise InvalidSpecException(e)

        # Database connection
        db = Database()
        connection = db.connect()
        if connection is None:
            raise DBConnectionException

        # Database manipulation
        ret = db.update_by_id(id, filename, SwaggerSpec.from_dict(spec_dict), content_type, raw)
        if ret is None:
            raise FileNotFoundException

        response = Success("Updated successfully")
        return make_response(jsonify(response), 200)

    except InvalidSpecException as e:
        e = Error(f"Invalid spec: {str(e)}")
        return make_response(jsonify(e), 400)

    except FileNotFoundException:
        e = Error("File not found")
        return make_response(jsonify(e), 404)

    except DBConnectionException:
        e = Error("Database connection error")
        return make_response(jsonify(e), 500)

    except Exception as e:
        return make_response(str(e), 503)
