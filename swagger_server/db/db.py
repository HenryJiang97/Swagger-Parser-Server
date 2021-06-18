import psycopg2
from psycopg2.extras import json
import uuid

from ..configs.config import POSTGRESQL_URI, TABLENAME

from ..models.success import Success
from ..models.error import Error
from ..models.swagger_spec import SwaggerSpec
from ..models.peek_data import PeekData


class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        """Establish connection with Postgres DB=
        """
        self.connection = psycopg2.connect(POSTGRESQL_URI)
        try:
            self.create_table()
        except psycopg2.errors.DuplicateTable:
            pass

    def select_all(self):
        """Select all entries in the DB

        :rtype: PeekData
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

    def select_by_id(self, id):
        """Select spec file by id from database.

        :param id: File unique id
        :type id:

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

    def insert(self, name, spec):
        """Insert new entry to the DB

        :param name: File name
        :type name: str
        :param spec: Specification file
        :type spec: SwaggerSpec

        :rtype: Success
        """
        psycopg2.extras.register_uuid()
        spec_id = uuid.uuid4()
        title = spec.info['title']
        version = spec.info['version']
        spec_dict = SwaggerSpec.to_dict(spec)

        try:
            with self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute(f"INSERT INTO {TABLENAME} VALUES (%s, %s, %s, %s, %s);",
                                   (spec_id, name, title, version, json.dumps(spec_dict)))
                return Success("Upload success")
        except psycopg2.errors.DuplicateFile:
            return Error("Duplicate files")

    def update_by_id(self, id, spec):
        """Update spec file by id from database.

        :param id: File unique id
        :type id:
        :param name: File name
        :type name: str
        :param spec: Specification file
        :type spec: SwaggerSpec

        :rtype: Success
        """
        version = spec.info['version']
        spec_dict = SwaggerSpec.to_dict(spec)

        try:
            with self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute(f"UPDATE {TABLENAME} SET version=(%s), spec=(%s) WHERE id='{id}';", (version, json.dumps(spec_dict)))
                return Success("Update success")
        except psycopg2.errors.SqlJsonMemberNotFound as e:
            return Error(e)

    def delete_by_id(self, id):
        """Delete spec file by id from database.

        :param id: File unique id
        :type id:

        :rtype: Success
        """
        try:
            with self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute(f"DELETE FROM {TABLENAME} WHERE id='{id}';")
                return Success("Entry deleted")
        except psycopg2.errors.SqlJsonMemberNotFound as e:
            return Error(e)

    def clear(self):
        """Delete all entries from the DB

        :rtype: Success
        """
        try:
            self.clear_table()
            return Success("Table cleared")
        except psycopg2.errors.NoData as e:
            return Error(e)

    def create_table(self):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(f"CREATE TABLE {TABLENAME} "
                               f"(id UUID UNIQUE, name TEXT, title TEXT, version TEXT, spec JSON);")

    def clear_table(self):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(f"DROP TABLE {TABLENAME};")
                cursor.execute(f"CREATE TABLE {TABLENAME} "
                               f"(id UUID UNIQUE, name TEXT, title TEXT, version TEXT, spec JSON);")
