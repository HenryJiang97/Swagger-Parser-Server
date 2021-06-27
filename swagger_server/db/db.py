import psycopg2
from psycopg2.extras import json
import uuid

from swagger_server.configs.config import POSTGRESQL_URI, TABLENAME

from swagger_server.models.success import Success
from swagger_server.models.error import Error
from swagger_server.models.swagger_spec import SwaggerSpec
from swagger_server.models.peek_data import PeekData
from swagger_server.models.spec_id import SpecId


class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        """Establish connection with Postgres DB=

        :rtype: Connection | None
        """
        self.connection = psycopg2.connect(POSTGRESQL_URI)
        try:
            self.create_table()
            return self.connection
        except psycopg2.errors.DuplicateTable:
            return self.connection
        except Exception as e:
            return None

    def select_all(self):
        """Select all entries in the DB

        :rtype: PeekData | Error
        """
        try:
            with self.connection:
                with self.connection.cursor() as cursor:
                    result = []
                    cursor.execute(f"SELECT id, name, version FROM {TABLENAME};")
                    response = cursor.fetchall()
                    for row in response:
                        result.append(
                            PeekData(
                                row[0],
                                row[1],
                                row[2]
                            )
                        )
                return result
        except ConnectionError as e:
            return Error(e)

    def insert(self, name, spec, content_type, raw):
        """Insert new entry to the DB

        :param name: File name
        :type name: str
        :param spec: Specification file
        :type spec: SwaggerSpec
        :param content_type: Raw file content type
        :type content_type: str
        :param raw: Raw file
        :type raw: binary

        :rtype: Success | Error | None
        """
        psycopg2.extras.register_uuid()
        spec_id = uuid.uuid4()
        title = spec.info['title']
        version = spec.info['version']
        spec_dict = SwaggerSpec.to_dict(spec)

        try:
            if self.select_by_title_and_version(title, version) is not None:
                return None
            with self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute(f"INSERT INTO {TABLENAME} VALUES (%s, %s, %s, %s, %s, %s, %s);",
                                   (spec_id, name, title, version, json.dumps(spec_dict), content_type, raw))
                return SpecId(spec_id)
        except psycopg2.errors.DuplicateFile:
            return Error("Duplicate files")

    def clear(self):
        """Delete all entries from the DB

        :rtype: Success | Error
        """
        try:
            self.clear_table()
            return Success("Table cleared")
        except psycopg2.errors.NoData as e:
            return Error(e)

    def select_by_title_and_version(self, title, version):
        """Select spec file by title from database.

        :param title: Spec title
        :type title: str
        :param version: Spec version
        :type version: str

        :rtype: binary
        """
        try:
            with self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute(f"SELECT raw FROM {TABLENAME} WHERE title='{title}' AND version='{version}';")
                    response = cursor.fetchall()
                    for row in response:
                        return SwaggerSpec.from_dict(row[0])
                return None
        except ConnectionError as e:
            return Error(e)

    def select_by_id(self, id):
        """Select raw file by id from database.

        :param id: File unique id
        :type id: str (uuid)

        :rtype: binary
        """
        try:
            with self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute(f"SELECT name, content_type, raw FROM {TABLENAME} WHERE id='{id}';")
                    response = cursor.fetchall()
                    for row in response:
                        return row
                return None
        except ConnectionError as e:
            return Error(e)

    def select_spec_by_id(self, id):
        """Select spec file by id from database.

        :param id: File unique id
        :type id: str (uuid)

        :rtype: SwaggerSpec
        """
        try:
            with self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute(f"SELECT spec FROM {TABLENAME} WHERE id='{id}';")
                    response = cursor.fetchall()
                    for row in response:
                        return SwaggerSpec.from_dict(row[0])
                return None
        except ConnectionError as e:
            return Error(e)

    def update_by_id(self, id, name, spec, content_type, raw):
        """Update spec file by id from database.

        :param id: File unique id
        :type id: str (uuid)
        :param name: File name
        :type name: str
        :param spec: Specification file
        :type spec: SwaggerSpec
        :param content_type: Raw file content type
        :type content_type: str
        :param raw: Raw file
        :type raw: binary

        :rtype: Success | Error | None
        """
        version = spec.info['version']
        spec_dict = SwaggerSpec.to_dict(spec)

        try:
            if self.select_by_id(id) is None:
                return None
            with self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute(f"UPDATE {TABLENAME} SET name=(%s), version=(%s), spec=(%s), content_type=(%s), raw=(%s) WHERE id='{id}';",
                                   (name, version, json.dumps(spec_dict), content_type, raw))
                return Success("Update success")
        except psycopg2.errors.SqlJsonMemberNotFound as e:
            return Error(e)

    def delete_by_id(self, id):
        """Delete spec file by id from database.

        :param id: File unique id
        :type id: str (uuid)

        :rtype: Success | Error | None
        """
        try:
            if self.select_by_id(id) is None:
                return None
            with self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute(f"DELETE FROM {TABLENAME} WHERE id='{id}';")
                return Success("Entry deleted")
        except psycopg2.errors.SqlJsonMemberNotFound as e:
            return Error(e)

    def create_table(self):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(f"CREATE TABLE {TABLENAME} "
                               f"(id UUID UNIQUE, name TEXT, title TEXT, version TEXT, spec JSON, "
                               f"content_type TEXT, raw bytea);")

    def clear_table(self):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(f"DROP TABLE {TABLENAME};")
                cursor.execute(f"CREATE TABLE {TABLENAME} "
                               f"(id UUID UNIQUE, name TEXT, title TEXT, version TEXT, spec JSON, "
                               f"content_type TEXT, raw bytea);")
