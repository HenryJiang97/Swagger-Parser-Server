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
        self.connection = psycopg2.connect(POSTGRESQL_URI)
        try:
            self.create_table()
        except psycopg2.errors.DuplicateTable:
            pass

    def select_all(self):
        try:
            # Save to db
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

    def insert(self, name, spec):
        psycopg2.extras.register_uuid()
        spec_id = uuid.uuid4()
        title = spec.info['title']
        version = spec.info['version']

        try:
            # Save to db
            with self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute(f"INSERT INTO {TABLENAME} VALUES (%s, %s, %s, %s, %s);",
                                   (spec_id, name, title, version, json.dumps(SwaggerSpec.to_dict(spec))))
                return Success("Upload success")
        except psycopg2.errors.DuplicateFile:
            return Error("Duplicate files")

    def clear(self):
        try:
            self.clear_table()
            return Success("Table cleared")
        except ConnectionError as e:
            return Error(e)

    def create_table(self):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(f"CREATE TABLE {TABLENAME} "
                               f"(id UUID UNIQUE, name TEXT, title TEXT, version TEXT, file JSON);")

    def clear_table(self):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(f"DROP TABLE {TABLENAME};")
                cursor.execute(f"CREATE TABLE {TABLENAME} "
                               f"(id UUID UNIQUE, name TEXT, title TEXT, version TEXT, file JSON);")
